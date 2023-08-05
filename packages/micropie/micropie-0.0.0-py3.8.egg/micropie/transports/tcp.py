import asyncio
from typing import Dict

from micropie.lib.enums import MessageType
from micropie.lib.exceptions import TransportError, ClientError
from micropie.lib.packer import Encoder
from micropie.rpc import Message
from micropie.transports.base import BaseTransport


class TcpTransport(BaseTransport):
    scheme = 'tcp'

    def __init__(self, url: str, ts_table: Dict[int, Encoder] = None, send_meta: dict = None):
        super().__init__(url, ts_table, send_meta)

        self._queue       = None
        self._server      = None
        self._should_stop = False


    async def interchange(self, message: Message, timeout: int = 0) -> Message:
        # validate message type
        if message.type not in (MessageType.REQUEST, MessageType.NOTIFY):
            raise TransportError(f"Invalid message type `{message.type.name}`")

        # create tcp client
        reader, writer = await asyncio.open_connection(host=self._location.host, port=self._location.port)

        # serialize and send message
        serialized = self.message_utils.serialize(
            self.message_utils.to_dict(message), partial=False
        )
        writer.write(serialized)
        writer.write_eof()
        await writer.drain()

        # get result
        result = None
        error = None
        try:
            if message.type != MessageType.NOTIFY:
                if not timeout:
                    result = await reader.read()
                else:
                    result = await asyncio.wait_for(reader.read(), timeout=timeout)
        except asyncio.TimeoutError as e:
            error = e

        # close client
        writer.close()
        await writer.wait_closed()

        if error:
            raise error

        if type(result) == bytes:
            if not len(result):
                raise ClientError('Remote connection closed unexpectedly')

            result = self.message_utils.build_from_deserialized(
                self.message_utils.deserialize(result, partial=False)
            )

        return result


    async def write(self, scope: dict, data: bytes):
        writer = scope['writer']

        # write and close
        writer.write(data)
        writer.write_eof()
        await writer.drain()
        writer.close()
        await writer.wait_closed()


    async def serve(self):
        # messages queue
        self._queue = asyncio.Queue()

        # server handler
        async def _handler(reader, writer):
            data = await reader.read()
            scope = { 'writer': writer }
            await self._queue.put((scope, data))

        self._server = await asyncio.start_server(_handler, host=self._location.host, port=self._location.port)
        socket_addr  = self._server.sockets[0].getsockname()

        # update location
        self._location.update_host(socket_addr[0])
        self._location.update_port(int(socket_addr[1]))

        # emit started info
        await self.on_started.emit({
            'transport': self.scheme,
            'location': self.location
        })

        # handle petitions
        while not self._should_stop:
            scope, data = await self._queue.get()
            try:
                deserialized = self.message_utils.deserialize(data)
            except Exception as e:
                error = TransportError(e)
                self.logger.exception(error)
            else:
                scope['_meta'] = deserialized['_meta']
                await self.receive(scope, deserialized)
            finally:
                self._queue.task_done()


    async def stop(self):
        self._should_stop = True
        await self._queue.join()
        if self._server:
            self._server.close()
            await self._server.wait_closed()
        await self.on_stopped.emit()