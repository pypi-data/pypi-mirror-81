import datetime
import random
from typing import Tuple, Any, Dict, Union

from micropie.lib.enums import MessageType, MessageMeta, ResultType
from micropie.lib.exceptions import MessageError
from micropie.lib.packer import Encoder, Packer


# noinspection PyShadowingBuiltins
class Message:

    def __init__(
            self,
            type   : MessageType,
            msgid  : int = None,
            method : str = None,
            params : Tuple[Tuple, dict] = ((), {}),
            result : Any = None,
            error  : Any = None,
            meta   : dict = None,
    ):
        from micropie import VERSION_STR

        meta = meta if meta else {}
        meta.update({
            MessageMeta.MICROPIE_VERSION: VERSION_STR,
            MessageMeta.MESSAGE_ID: msgid,
            MessageMeta.MESSAGE_TYPE: MessageType(type),
            MessageMeta.ISSUE_DATETIME: datetime.datetime.utcnow().replace(
                tzinfo=datetime.timezone.utc).isoformat('T', 'seconds')
        })
        self._meta = meta

        rpc  = {
            'method': method,
            'params': params,
            'result': result,
            'error' : error
        }

        # clean rpc according message type
        if type in (MessageType.REQUEST, MessageType.NOTIFY):
            rpc.pop('error', None)
            rpc.pop('result', None)
        elif type == MessageType.RESPONSE:
            rpc.pop('method', None)
            rpc.pop('params', None)

        self._rpc = rpc

    @property
    def meta(self):
        return self._meta

    @property
    def type(self):
        return MessageType(self._meta[MessageMeta.MESSAGE_TYPE])

    @property
    def msgid(self):
        return self._meta[MessageMeta.MESSAGE_ID]

    @property
    def method(self):
        return self._rpc.get('method')

    @property
    def method_args(self):
        return self._rpc.get('params', (None, None))[0]

    @property
    def method_kwargs(self):
        return self._rpc.get('params', (None, None))[1]

    def add_meta(self, meta: str, value):
        self._meta[meta] = value

    def get_result(self, raise_error=True):
        if raise_error:
            error = self._rpc.get('error')
            if error:
                raise error
        return self._rpc.get('result')


class MessageUtils:

    def __init__(self, ts_table: Dict[int, Encoder] = None):
        self._ts_table = ts_table

    def _serialize_rpc(self, rpc: dict) -> bytes:
        """Serialize only rpc part. Can raise Error"""
        return Packer.from_ts_table(self._ts_table).packb(rpc)

    def _deserialize_rpc(self, data: bytes) -> dict:
        """Deserialize only rpc part. Can raise Error"""
        return Packer.from_ts_table(self._ts_table).unpackb(data)

    def to_dict(self, message: Message) -> dict:
        return {
            '_meta': getattr(message, '_meta'),
            'rpc'  : getattr(message, '_rpc')
        }

    def serialize(self, data: dict, partial: bool = True) -> Union[bytes, dict]:
        """
        Serialize message

        :param data: message dict (usually generated with .to_dict())
        :param partial: indicate when serialize or not `rpc` part
        :return if partial return a dict with `rpc` part not serialized, else returns bytes (all serialized)
        """
        serialized = data.copy()

        if type(serialized['_meta']) == dict:
            serialized['_meta'] = Packer().packb(data['_meta'])

        if not partial:
            serialized['rpc'] = self._serialize_rpc(serialized['rpc'])
            return Packer().packb(serialized)

        return serialized

    def deserialize(self, data: Union[bytes, dict], partial: bool = True) -> dict:
        """Deserialize message. Can raise Error"""
        data_type = type(data)

        if data_type == bytes:
            deserialized = Packer().unpackb(data)
            deserialized['_meta'] = Packer().unpackb(deserialized['_meta'])
        elif data_type == dict:
            deserialized = data.copy()
        else:
            raise TypeError(f'Invalid data type `{data_type}`')

        if not partial:
            deserialized['rpc'] = self._deserialize_rpc(deserialized['rpc'])

        return deserialized

    def build_from_deserialized(self, deserialized: dict) -> Message:
        """Create message from deserialized data. Can raise Error"""
        meta = deserialized['_meta']
        rpc  = deserialized['rpc']

        if type(rpc) == bytes:
            raise MessageError('Can not build message from partial deserialized')

        return Message(type=meta[MessageMeta.MESSAGE_TYPE], msgid=meta[MessageMeta.MESSAGE_ID], meta=meta, **rpc)

    def build_request(self, method: str, args: Tuple = None, kwargs: dict = None, meta: dict = None) -> Message:
        msgid  = random.randrange(1, 1000)
        params = ( args if args else tuple(), kwargs if kwargs else dict() )
        return Message(type=MessageType.REQUEST, msgid=msgid, method=method, params=params, meta=meta)

    def build_notify(self, method: str, args: Tuple = None, kwargs: dict = None, meta: dict = None) -> Message:
        params = ( args if args else tuple(), kwargs if kwargs else dict() )
        return Message(type=MessageType.NOTIFY, method=method, params=params, meta=meta)

    def build_response(self, msgid: int, result = None, meta: dict = None) -> Message:
        meta = meta or {}
        meta[MessageMeta.RESULT_TYPE] = ResultType.SINGLE_RESULT
        return Message(type=MessageType.RESPONSE, msgid=msgid, result=result, meta=meta)

    def build_response_error(self, msgid: int, error: Exception = None, meta: dict = None) -> Message:
        meta = meta or {}
        meta[MessageMeta.RESULT_TYPE] = ResultType.ERROR_RESULT
        return Message(type=MessageType.RESPONSE, msgid=msgid, error=error, meta=meta)
