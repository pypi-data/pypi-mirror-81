import asyncio
from typing import Dict
from uuid import uuid4

from micropie.lib.enums import MessageMeta, MessageType
from micropie.lib.exceptions import TransportError, ClientError
from micropie.lib.packer import Encoder
from micropie.rpc import Message
from micropie.transports.base import BaseTransport

try:
    import aio_pika
    from aio_pika import __version__ as aiopika_version
except ImportError:
    aiopika_version = '0'

_AIOPIKA_VERSION = '.'.join(map(str, (6,6,1)))


class AmqpTransport(BaseTransport):
    scheme = 'amqp'

    def __init__(self, url: str, ts_table: Dict[int, Encoder] = None, send_meta: dict = None):
        super().__init__(url, ts_table, send_meta)

        # check aioredis version
        if aiopika_version < _AIOPIKA_VERSION:  # pragma: no cover
            raise ImportError("AmqpTransport requires aio-pika package"
                              " (version >= {})".format(_AIOPIKA_VERSION))

        self._connection = None
        self._exchange = None
        self._queue = None

    async def interchange(self, message: Message, timeout: int = 0) -> Message:
        # validate message type
        if message.type not in (MessageType.REQUEST, MessageType.NOTIFY):
            raise TransportError(f"Invalid message type `{message.type.name}`")

        # create feedback and update message meta
        feedback_q = f'rpc-proxy:{uuid4().hex}'
        message.add_meta(MessageMeta.FEEDBACK_TO, feedback_q)

        # create connection and channel
        connection = await aio_pika.connect(self.location)
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)

        # create exchange and queue
        exchange = await channel.declare_exchange("micropie", aio_pika.ExchangeType.DIRECT, auto_delete=True)
        queue = await channel.declare_queue(feedback_q, exclusive=True)
        await queue.bind(exchange, routing_key=feedback_q)

        # serialize and publish message
        serialized = self.message_utils.serialize(
            self.message_utils.to_dict(message), partial=False
        )
        await exchange.publish(aio_pika.Message(body=serialized), routing_key=self._location.channel)

        async def reader():
            async with queue.iterator() as q_iter:
                async for in_message in q_iter:
                    await in_message.ack()
                    return in_message.body

        # get result
        result = None
        error = None
        try:
            if message.type != MessageType.NOTIFY:
                if not timeout:
                    result = await reader()
                else:
                    result = await asyncio.wait_for(reader(), timeout=timeout)
        except asyncio.TimeoutError as e:
            error = e

        # close client
        await queue.unbind(exchange, feedback_q)
        await connection.close()

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
        feedback_ch = scope['_meta'][MessageMeta.FEEDBACK_TO]
        await self._exchange.publish(aio_pika.Message(body=data), routing_key=feedback_ch)


    async def serve(self):
        # create channel
        if not self._location.channel:
            self._location.update_channel(f'rpc:{uuid4().hex}')

        # create connection and channel
        self._connection = await aio_pika.connect_robust(self._location.url)
        channel = await self._connection.channel()
        await channel.set_qos(prefetch_count=1)

        # create exchange and queue
        self._exchange = await channel.declare_exchange("micropie", aio_pika.ExchangeType.DIRECT, auto_delete=True)
        self._queue = await channel.declare_queue(self._location.channel, exclusive=True)
        await self._queue.bind(self._exchange, routing_key=self._location.channel)

        # emit started info
        await self.on_started.emit({
            'transport': self.scheme,
            'location': self.location
        })

        # handle petitions
        async with self._queue.iterator() as q_iter:
            async for message in q_iter:
                data = message.body
                try:
                    deserialized = self.message_utils.deserialize(data)
                except Exception as e:
                    error = TransportError(e)
                    self.logger.exception(error)
                else:
                    await self.receive({'_meta': deserialized['_meta']}, deserialized)
                finally:
                    await message.ack()


    async def stop(self):
        if self._queue and self._exchange:
            await self._queue.unbind(self._exchange, self._location.channel)
        if self._connection:
            await self._connection.close()
        await self.on_stopped.emit()