import logging
from typing import Dict, Mapping
from uuid import uuid4

from micropie.config import TRANSPORTS
from micropie.lib import signals, Location, importer
from micropie.lib.enums import MessageMeta, MessageType
from micropie.lib.exceptions import TransportError, RemoteError
from micropie.lib.packer import Encoder
from micropie.rpc.message import MessageUtils, Message


# noinspection DuplicatedCode
class BaseTransport:
    scheme = None

    def __init__(self, url: str, ts_table: Dict[int, Encoder] = None, send_meta: dict = None):
        loc = Location(url)

        if not self.scheme:
            raise TransportError('Transport.scheme not defined')

        if self.scheme != loc.scheme:
            raise TransportError(f'Invalid url scheme `{loc.scheme}`')

        self._location = loc
        self.message_utils = MessageUtils(ts_table)
        self._send_meta = send_meta or {}
        self.logger = logging.getLogger('micropie.transport')

        # signals
        self.on_started = signals.signal(name=uuid4().hex)
        self.on_message = signals.signal(name=uuid4().hex)
        self.on_stopped = signals.signal(name=uuid4().hex)

    @property
    def location(self):
        return self._location.url

    async def interchange(self, message: Message, timeout: int = 0) -> Message:
        raise NotImplementedError

    async def receive(self, scope: dict, deserialized: dict):
        self.logger.debug(f'RECV: {scope["_meta"]}')

        # validate message type
        message_type = MessageType(scope['_meta'][MessageMeta.MESSAGE_TYPE])
        if message_type not in (MessageType.REQUEST, MessageType.NOTIFY):
            error = TransportError(f"Invalid message type `{message_type.name}`")
            self.logger.exception(error)
            await self.send_error(scope, error)
            return

        # full deserialization
        try:
            deserialized = self.message_utils.deserialize(deserialized, partial=False)
        except Exception as e:
            await self.send_error(scope, e)
            return

        # function to send response
        async def sender(message: Message):
            scope['_send_meta'] = message.meta
            await self.send(
                scope=scope,
                serialized=self.message_utils.serialize(
                    data=self.message_utils.to_dict(message)
                )
            )

        # emit message and sender function
        await self.on_message.emit(self.message_utils.build_from_deserialized(deserialized), sender)

    async def send(self, scope: dict, serialized: dict):
        # full serialization
        try:
            serialized = self.message_utils.serialize(serialized, partial=False)
        except Exception as e:
            self.logger.exception(e)
            return await self.send_error(scope, e)

        self.logger.debug(f'SEND: {scope["_send_meta"]}')
        await self.write(scope, data=serialized)

    async def send_error(self, scope: dict, error: Exception):
        await self.send(
            scope=scope,
            serialized=self.message_utils.serialize(
                self.message_utils.to_dict(
                    self.message_utils.build_response_error(
                        msgid=scope['_meta'][MessageMeta.MESSAGE_ID],
                        error=RemoteError(error),
                        meta=self._send_meta
                    )
                )
            )
        )

    async def write(self, scope: dict, data: bytes):
        raise NotImplementedError

    async def serve(self):
        raise NotImplementedError

    async def stop(self):
        raise NotImplementedError


def build_transport_from_url(url: str, ts_table: Mapping[int, Encoder]) -> BaseTransport:
    loc = Location(url)

    if loc.scheme not in TRANSPORTS.keys():
        raise TransportError(f"Transport not defined for scheme `{loc.scheme}`")

    transport_cls = importer.import_from_string( TRANSPORTS[loc.scheme] )
    return transport_cls(url, ts_table)



