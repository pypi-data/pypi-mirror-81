import argparse
import asyncio
import inspect
import os
import signal
import sys
import uuid
from typing import Callable, Dict

from micropie.config import LOOP_SETUPS, LOG_LEVELS, Config
from micropie.lib import Stream
from micropie.lib.enums import MessageMeta, MessageType, ResultType, ServerFunction, SenderType
from micropie.lib.exceptions import RpcError, RemoteError, ServiceError
from micropie.rpc import Message, rpc_client, rpc_proxy
from micropie.transports.base import BaseTransport


parser = argparse.ArgumentParser(prog='micropie', description='A micro framework for microservices')
parser.add_argument(dest='cls', help='Service class definition')
parser.add_argument('-l', '--log-level', default='info', choices=LOG_LEVELS.keys(), help='Logs level to use')
parser.add_argument('-t', '--transport-url', default='tcp://0.0.0.0', help='Service transport url to use')
parser.add_argument('-p', '--loop', default='auto', choices=LOOP_SETUPS.keys(), help='Event loop type to use')
parser.add_argument('-r', '--registry', default=None, help='Services registry url')
parser.add_argument('-o', '--registry-timeout', type=int, default=5, help='Services registry max timeout for request')
parser.add_argument('-b', '--heartbeats-delay', type=int, default=120, help='Service heartbeats delay time')


def main():
    sys.path.insert(0, ".")
    args = parser.parse_args()
    cls = args.cls

    kwargs = {
        'loop': args.loop,
        'transport_url': args.transport_url,
        'registry_url': args.registry,
        'registry_timeout': args.registry_timeout,
        'heartbeats_delay': args.heartbeats_delay,
        'log_level': args.log_level,
    }

    run(cls, **kwargs)


# noinspection DuplicatedCode
def run(
    cls,
    transport_url: str = 'tcp://0.0.0.0',
    registry_url: str = None,
    registry_timeout: int = 5,
    heartbeats_delay: int = 120,
    loop: str = 'auto',
    log_level: str = 'info'
):
    config = Config(
        cls,
        transport_url=transport_url,
        registry_url=registry_url,
        registry_timeout=registry_timeout,
        heartbeats_delay=heartbeats_delay,
        loop=loop,
        log_level=log_level
    )
    config.load()

    server = Service(config=config)
    server.run()


# noinspection DuplicatedCode,PyMethodMayBeStatic,PyTypeChecker
class Service:

    def __init__(self, config: Config):
        assert config.loaded
        self.config = config
        self.logger = config.logger_instance
        self.loop = None
        self.transport: BaseTransport = None
        self.service = None
        self.instance = uuid.uuid4().hex
        self.dependencies = set()
        self.send_meta = {
            MessageMeta.SENDER_ID: self.instance,
            MessageMeta.SENDER_TYPE: SenderType.SERVICE,
            MessageMeta.SENDER_NAME: self.config.name
        }
        self._active_streams: Dict[str, Stream] = {}
        self._registered = False

    @property
    def server_info(self):
        return self._server_info()

    def _server_info(self):
        from micropie import VERSION_STR

        info = {
            'micropie.version': VERSION_STR,
            'service.name': self.config.name,
            'service.description': self.config.desc,
            'service.dependencies': list(self.dependencies)
        }

        return info

    def _rpc_handler(self, func: Callable, message: Message, *args, **kwargs):
        sig = inspect.signature(func)
        args_idx = 0
        for name, param in sig.parameters.items():
            # inject Message into kwargs
            if param.annotation == Message:
                kwargs[name] = message

            # migrate args to kwargs
            elif name not in kwargs and args_idx < len(args):
                kwargs[name] = args[args_idx]
                args_idx += 1

        arguments = sig.bind(**kwargs).arguments
        return func(**arguments)

    async def _on_started(self, info):
        out = sys.stdout
        ln = '\n'
        out.write('=' * 23 + ln)
        out.write(' ' * 5 + 'MICROPIE ' + f'{self.server_info["micropie.version"]}' + ln)
        out.write('=' * 23 + ln)
        out.write(' * ' + f'pid: {os.getpid()}' + ln)
        out.write(' * ' + f'standalone: {self.config.registry_url is None}' + ln)
        out.write(' * ' + f'service: {self.config.name}' + ln)
        out.write(' * ' + f'description: {self.config.desc}' + ln)
        out.write(' * ' + f'instance: {self.instance}' + ln)
        out.write(' * ' + f'transport: {self.transport.scheme}' + ln)
        out.write(' * ' + f'loop: {self.config.loop}' + ln)
        out.write(' * ' + f'logs: {self.config.log_level.upper()}' + ln)

        if self.config.registry_url:
            out.write(' * ' + f'registry-url: {self.config.registry_url}' + ln)
            out.write(' * ' + f'heartbeats-delay: {self.config.heartbeats_delay}s' + ln)
            if self.dependencies:
                out.write(' * ' + f'dependencies: {list(self.dependencies)}' + ln)

            # check service dependencies
            for i, service in enumerate(self.dependencies):
                try:
                    response = await rpc_client(
                        service_url=self.config.registry_url,
                        message_type=MessageType.REQUEST,
                        method='lookup',
                        args=(service, 0.01),
                        timeout=self.config.registry_timeout,
                        send_meta=self.send_meta
                    )
                    services = response.get_result()

                    if not services:
                        raise Exception(f'Service {service} not found or unavailable')

                    self.logger.info(f'DEPENDENCY-CHECK <{i + 1}/{len(self.dependencies)}>: {service} [ok]')
                except Exception as e:
                    self.logger.error(f'DEPENDENCY-CHECK <{i + 1}/{len(self.dependencies)}>: {service} [fail] {e}')
                    asyncio.ensure_future(self._stop(), loop=self.loop)
                    return

            # registering service
            try:
                await rpc_client(
                    service_url=self.config.registry_url,
                    message_type=MessageType.NOTIFY,
                    method='registrar',
                    args=(self.instance, self.config.name, self.transport.location),
                    timeout=self.config.registry_timeout,
                    send_meta=self.send_meta
                )
                self.logger.info(f'REGISTRY: [ok] {self.instance}/{self.config.name}')
                self._registered = True
            except Exception as e:
                self.logger.error(f'REGISTRY: [fail] {e}')
                asyncio.ensure_future(self._stop(), loop=self.loop)
                return

            # service heartbeats task function
            # noinspection PyShadowingNames
            async def _heartbeats():
                while True:
                    await asyncio.sleep(self.config.heartbeats_delay)
                    try:
                        await rpc_client(
                            service_url=self.config.registry_url,
                            message_type=MessageType.NOTIFY,
                            method='heartbeat',
                            args=(self.instance, self.config.name, self.transport.location),
                            timeout=self.config.registry_timeout,
                            send_meta=self.send_meta
                        )
                        self.logger.info(f'HEARTBEAT: [ok] {self.instance}/{self.config.name}')
                    except Exception as e:
                        self.logger.error(f'HEARTBEAT: [fail] {e}')

            # start heartbeats task
            asyncio.ensure_future(_heartbeats(), loop=self.loop)

        # print info frame
        out.flush()
        self.logger.info(f'STARTED listen on: {info["location"]} (Press CTRL+C to quit)')

    async def _on_message(self, request: Message, send):
        try:
            ############################
            # *** Process Request ***
            ############################

            # call server info
            if request.method == ServerFunction.INFO:
                result = self._server_info()

            # call server ping
            elif request.method == ServerFunction.PING:
                result = 'PONG'

            # call stream next value
            elif request.method == ServerFunction.STREAM_NEXT:
                if MessageMeta.STREAM_ID not in request.meta:
                    raise ServiceError('STREAM_ID is required into request metadata message')
                result = await self._active_streams[request.meta[MessageMeta.STREAM_ID]].next()

            # call service function
            else:
                # check if function exist
                service_func = getattr(self.service, request.method, None)
                if not service_func:
                    raise RpcError(f'Function {request.method} not found')

                # check if function is private
                if request.method.startswith('_'):
                    raise RpcError(f'Protected/Private function {request.method} can not be called')

                # check if really is a function
                if not inspect.ismethod(service_func):
                    raise RpcError(f'{request.method} is not a function')

                # call service function
                result = self._rpc_handler(service_func, request, *request.method_args, **request.method_kwargs)

            ###########################
            # *** Process Result ***
            ###########################

            # create stream response message
            if Stream.can_stream(result) or request.method == ServerFunction.STREAM_NEXT:
                stream_id = request.meta.get(MessageMeta.STREAM_ID, uuid.uuid4().hex)

                # add result as new active stream
                if request.method != ServerFunction.STREAM_NEXT:
                    self._active_streams[stream_id] = Stream.create_stream(result)
                    # get next result from stream
                    result = await self._active_streams[stream_id].next()

                # check result is not a generator again (generator of generators)
                if Stream.can_stream(result):
                    raise ServiceError('A stream cannot be returned while another is active, due to '
                                       'micropie does not support generator of generators as result '
                                       'for functions')

                # Result could be an exception
                if isinstance(result, Exception):
                    response = self.transport.message_utils.build_response_error(
                        msgid=request.meta[MessageMeta.MESSAGE_ID],
                        error=RemoteError(result),
                        meta=self.send_meta
                    )
                else:
                    response = self.transport.message_utils.build_response(
                        msgid=request.meta[MessageMeta.MESSAGE_ID],
                        result=result,
                        meta=self.send_meta
                    )

                response.add_meta(MessageMeta.RESULT_TYPE, ResultType.STREAM_RESULT)
                response.add_meta(MessageMeta.STREAM_ID, stream_id)
                response.add_meta(MessageMeta.STREAM_WORKER_URL, self.transport.location)
                response.add_meta(MessageMeta.STREAM_HAS_NEXT, await self._active_streams[stream_id].has_next)

                # discard empty stream
                if not (await self._active_streams[stream_id].has_next):
                    self._active_streams.pop(stream_id, None)

            # create single response message
            else:
                result = (await result) if inspect.iscoroutine(result) else result
                response = self.transport.message_utils.build_response(
                    msgid=request.meta[MessageMeta.MESSAGE_ID],
                    result=result,
                    meta=self.send_meta
                )
        except Exception as e:
            self.logger.exception(e)

            # create error response message
            response = self.transport.message_utils.build_response_error(
                msgid=request.meta[MessageMeta.MESSAGE_ID],
                error=RemoteError(e),
                meta=self.send_meta
            )

        # send response
        if request.type != MessageType.NOTIFY:
            await send(response)

    async def _on_stopped(self):
        # unregistry service
        if self.config.registry_url and self._registered:
            try:
                await rpc_client(
                    service_url=self.config.registry_url,
                    message_type=MessageType.NOTIFY,
                    method='unregistry',
                    args=(self.instance,),
                    timeout=self.config.registry_timeout,
                    send_meta=self.send_meta
                )
                self.logger.info(f'UNREGISTRY: [ok] {self.instance}/{self.config.name}')
            except Exception as e:
                self.logger.error(f'UNREGISTRY: [fail] {e}')

        self.logger.info('STOPPED')

    def _handle_exceptions(self, loop, context):
        try:
            if context.get('exception'):
                raise context['exception']
        except Exception as e:
            self.logger.exception(e)
        else:
            self.logger.error(context["message"])
        finally:
            asyncio.ensure_future(self._stop(), loop=loop)

    def run(self):
        # setup event loop
        self.config.setup_event_loop()
        self.loop = asyncio.get_event_loop()
        self.loop.set_exception_handler(self._handle_exceptions)

        for sig in (signal.SIGHUP, signal.SIGTERM, signal.SIGINT):
            self.loop.add_signal_handler(sig, lambda: asyncio.ensure_future(self._stop(), loop=self.loop))

        # setup transport
        self.transport = self.config.loaded_transport_cls(
            url=self.config.transport_url,
            ts_table=self.config.ts_table,
            send_meta=self.send_meta
        )

        self.transport.on_started.connect(self._on_started)
        self.transport.on_message.connect(self._on_message)
        self.transport.on_stopped.connect(self._on_stopped)

        # setup proxies
        proxies = filter(
            lambda p: type(getattr(self.config.loaded_service_cls, p)) == rpc_proxy,
            dir(self.config.loaded_service_cls)
        )
        for proxy in proxies:
            if not self.config.registry_url:
                self.logger.error("Can not configure rpc_proxy into standalone service, please define registry url")
                sys.exit(1)

            proxy = getattr(self.config.loaded_service_cls, proxy)

            if proxy.service == self.config.name:
                self.logger.error("Can not configure self rpc_proxy into service")
                sys.exit(1)

            self.dependencies.add(proxy.service)
            proxy.configure(self.config.registry_url, self.config.registry_timeout, self.send_meta)

        # create service object
        self.service = self.config.loaded_service_cls()

        # start serving
        asyncio.ensure_future(self.transport.serve(), loop=self.loop)
        self.loop.run_forever()

    async def _stop(self):
        await self.transport.stop()
        # cancel active tasks
        tasks = [t for t in asyncio.all_tasks(loop=self.loop) if t is not asyncio.current_task()]
        [task.cancel() for task in tasks]
        await asyncio.gather(*tasks, return_exceptions=True)
        self.loop.stop()
