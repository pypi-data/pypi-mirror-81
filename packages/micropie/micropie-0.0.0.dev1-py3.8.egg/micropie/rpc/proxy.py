from typing import Dict, Mapping

from micropie.lib.enums import MessageType, MessageMeta, ResultType, ServerFunction
from micropie.lib.exceptions import ProxyError
from micropie.lib.packer import Encoder
from micropie.rpc import rpc_client


class _RpcProxy:

    def __init__(
            self,
            service: str,
            timeout: int = None,
            ts_table: Dict[int, Encoder] = None
    ):
        self.service = service
        self.timeout = timeout
        self.ts_table = ts_table
        self.registry_url = None
        self.registry_timeout = None
        self.send_meta = None

    def configure(self, registry_url: str, registry_timeout: int = None, send_meta: Mapping  = None):
        self.registry_url = registry_url
        self.registry_timeout = registry_timeout
        self.send_meta = send_meta

    async def instances(self, do_raise=True):
        caller = _CallProxy(self, method='')
        return await caller.instances(do_raise)

    async def info(self, do_raise=True):
        caller = _CallProxy(self, method='')
        return await caller.info(do_raise)

    async def ping(self, do_raise=False):
        caller = _CallProxy(self, method='')
        return await caller.ping(do_raise)

    async def is_alive(self):
        caller = _CallProxy(self, method='')
        return await caller.is_alive()

    def __getattr__(self, method):
        if not self.registry_url:
            raise ProxyError('Not configured rpc_proxy, call rpc_proxy.configure() first')

        return _CallProxy(self, method=method)

    __getitem__ = __getattr__


# noinspection DuplicatedCode
class _CallProxy:

    def __init__(self, parent: _RpcProxy, method: str):
        self.parent = parent
        self.method = method

    async def _get_service_url(self, do_raise=True):
        try:
            response = await rpc_client(
                service_url=self.parent.registry_url,
                message_type=MessageType.REQUEST,
                method='get_worker',
                args=(self.parent.service,),
                timeout=self.parent.registry_timeout,
                send_meta=self.parent.send_meta
            )

            worker = response.get_result(raise_error=do_raise)

            if not worker:
                if do_raise:
                    raise ProxyError(f'Service {self.parent.service} not found or unavailable')
                return

            return worker['url']
        except ConnectionError or OSError:
            raise ProxyError(f'Registry unavailable at {self.parent.registry_url}') from None
        except ProxyError as e:
            raise e from None
        except Exception as e:
            raise ProxyError(e) from None

    async def call(self, *args, **kwargs):
        service_url = await self._get_service_url()

        response = await rpc_client(
            service_url=service_url,
            message_type=MessageType.REQUEST,
            method=self.method,
            args=args,
            kwargs=kwargs,
            timeout=self.parent.timeout,
            ts_table=self.parent.ts_table,
            send_meta=self.parent.send_meta
        )

        # check result type
        if response.meta[MessageMeta.RESULT_TYPE] == ResultType.STREAM_RESULT:
            raise ProxyError(f'Invalid result type {ResultType.STREAM_RESULT.name}, use stream(...) '
                             f'function to handle this result type')

        return response.get_result()

    async def stream(self, *args, **kwargs):
        service_url = await self._get_service_url()

        response = await rpc_client(
            service_url=service_url,
            message_type=MessageType.REQUEST,
            method=self.method,
            args=args,
            kwargs=kwargs,
            timeout=self.parent.timeout,
            ts_table=self.parent.ts_table,
            send_meta=self.parent.send_meta
        )

        # response can be an error response
        if response.meta[MessageMeta.RESULT_TYPE] == ResultType.ERROR_RESULT:
            response.get_result()  # raise error

        # check result type
        if response.meta[MessageMeta.RESULT_TYPE] == ResultType.SINGLE_RESULT:
            raise ProxyError(f'Invalid result type {ResultType.SINGLE_RESULT.name}, use call(...) '
                             f'function to handle this result type')

        stream_id = response.meta[MessageMeta.STREAM_ID]
        worker_url = response.meta[MessageMeta.STREAM_WORKER_URL]
        has_next = response.meta[MessageMeta.STREAM_HAS_NEXT]

        # return 1st result
        yield response.get_result()

        while has_next:
            send_meta = { MessageMeta.STREAM_ID: stream_id }
            send_meta.update(self.parent.send_meta)

            response = await rpc_client(
                service_url=worker_url,
                message_type=MessageType.REQUEST,
                method=ServerFunction.STREAM_NEXT,
                timeout=self.parent.timeout,
                ts_table=self.parent.ts_table,
                send_meta=send_meta
            )
            has_next = response.meta[MessageMeta.STREAM_HAS_NEXT]

            yield response.get_result()

    async def notify(self, *args, **kwargs):
        service_url = await self._get_service_url()

        await rpc_client(
            service_url=service_url,
            message_type=MessageType.NOTIFY,
            method=self.method,
            args=args,
            kwargs=kwargs,
            timeout=self.parent.timeout,
            ts_table=self.parent.ts_table,
            send_meta=self.parent.send_meta
        )

    async def instances(self, do_raise=True):
        response = await rpc_client(
            service_url=self.parent.registry_url,
            message_type=MessageType.REQUEST,
            method='lookup',
            args=(self.parent.service,),
            timeout=self.parent.registry_timeout,
            send_meta=self.parent.send_meta
        )
        return response.get_result(raise_error=do_raise)

    async def info(self, do_raise = True):
        service_url = await self._get_service_url(do_raise=do_raise)

        if service_url:
            response = await rpc_client(
                service_url=service_url,
                message_type=MessageType.REQUEST,
                method=ServerFunction.INFO,
                timeout=self.parent.timeout,
                ts_table=self.parent.ts_table,
                send_meta=self.parent.send_meta
            )
            return response.get_result(raise_error=do_raise)

    async def ping(self, do_raise = False):
        service_url = await self._get_service_url(do_raise=do_raise)

        if service_url:
            response = await rpc_client(
                service_url=service_url,
                message_type=MessageType.REQUEST,
                method=ServerFunction.PING,
                timeout=self.parent.timeout,
                ts_table=self.parent.ts_table,
                send_meta=self.parent.send_meta
            )
            return response.get_result(raise_error=do_raise)

    async def is_alive(self):
        return (await self.ping()) == 'PONG'


rpc_proxy = _RpcProxy
