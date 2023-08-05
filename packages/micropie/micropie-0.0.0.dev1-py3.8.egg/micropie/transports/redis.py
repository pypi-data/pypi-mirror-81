import asyncio
from typing import Dict
from uuid import uuid4

from micropie.lib.enums import MessageMeta, MessageType
from micropie.lib.exceptions import TransportError, ClientError
from micropie.lib.packer import Encoder
from micropie.rpc import Message
from micropie.transports.base import BaseTransport

try:
    import aioredis
    from aioredis import __version__ as aioredis_version
except ImportError:
    aioredis_version = '0'

_AIOREDIS_VERSION = '.'.join(map(str, (1,3,1)))


class RedisTransport(BaseTransport):
    scheme = 'redis'

    def __init__(self, url: str, ts_table: Dict[int, Encoder] = None, send_meta: dict = None):
        super().__init__(url, ts_table, send_meta)

        # check aioredis version
        if aioredis_version < _AIOREDIS_VERSION:  # pragma: no cover
            raise ImportError("RedisTransport requires aioredis package"
                              " (version >= {})".format(_AIOREDIS_VERSION))

        self._redis_client = None


    async def interchange(self, message: Message, timeout: int = 0) -> Message:
        # validate message type
        if message.type not in (MessageType.REQUEST, MessageType.NOTIFY):
            raise TransportError(f"Invalid message type `{message.type.name}`")

        # create feedback and update message meta
        feedback_ch = f'rpc-proxy:{uuid4().hex}'
        message.add_meta(MessageMeta.FEEDBACK_TO, feedback_ch)

        # create redis pool and subscribe to channel
        redis_client = await aioredis.create_redis_pool(self.location)
        channel, = await redis_client.subscribe(channel=feedback_ch)

        # serialize and publish message
        serialized = self.message_utils.serialize(
            self.message_utils.to_dict(message), partial=False
        )
        await redis_client.publish(self._location.channel, message=serialized)

        # channel reader
        async def reader():
            await channel.wait_message()
            return await channel.get()

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
        redis_client.close()
        await redis_client.wait_closed()

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
        await self._redis_client.publish(feedback_ch, data)


    async def serve(self):
        # create channel
        if not self._location.channel:
            self._location.update_channel(f'rpc:{uuid4().hex}')

        # create client
        self._redis_client = await aioredis.create_redis_pool(self._location.url)
        channel, = await self._redis_client.subscribe(self._location.channel)

        # emit started info
        await self.on_started.emit({
            'transport': self.scheme,
            'location': self.location
        })

        # handle petitions
        while await channel.wait_message():
            data = await channel.get()
            try:
                deserialized = self.message_utils.deserialize(data)
            except Exception as e:
                error = TransportError(e)
                self.logger.exception(error)
            else:
                await self.receive({'_meta': deserialized['_meta']}, deserialized)


    async def stop(self):
        if self._redis_client:
            await self._redis_client.unsubscribe(self._location.channel)
            self._redis_client.close()
            await self._redis_client.wait_closed()
        await self.on_stopped.emit()
