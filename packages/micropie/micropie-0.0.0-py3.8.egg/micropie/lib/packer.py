import pickle
from collections import ChainMap
from datetime import date, datetime, time, tzinfo, timedelta
from functools import partial
from typing import Callable, Any, Dict, Mapping

import msgpack
from msgpack import ExtType

from micropie.lib.enums import MessageType, ResultType
from micropie.lib.exceptions import RemoteError


class Encoder:
    def __init__(self, cls, pack: Callable[[Any], bytes] = None, unpack: Callable[[bytes], Any] = None):
        self._type = cls
        self._pack = pack if pack else partial(pickle.dumps, protocol=pickle.HIGHEST_PROTOCOL)
        self._unpack = unpack if unpack else pickle.loads

    @property
    def type(self):
        return self._type

    def pack(self, obj):
        return self._pack(obj)

    def unpack(self, packed: bytes):
        return self._unpack(packed)


_DEFAULT_TS_TABLE = {
    127: Encoder(
        RemoteError,
        pack=lambda obj: msgpack.packb(str(obj)),
        unpack=lambda raw: RemoteError( msgpack.unpackb(raw) )
    ),
    126: Encoder(
        MessageType,
        pack=lambda obj: msgpack.packb(obj.value),
        unpack=lambda raw: MessageType( msgpack.unpackb(raw) )
    ),
    125: Encoder(
        ResultType,
        pack=lambda obj: msgpack.packb(obj.value),
        unpack=lambda raw: ResultType( msgpack.unpackb(raw) )
    ),
    124: Encoder(date),
    123: Encoder(datetime),
    122: Encoder(time),
    121: Encoder(timedelta),
    120: Encoder(tzinfo)
}


class Packer:

    @classmethod
    def from_ts_table(cls, ts_table: Dict[int, Encoder]):
        return cls(ts_table=ts_table)

    def __init__(self, *, ts_table: Mapping[int, Encoder] = None):
        if ts_table is None:
            translation_table = _DEFAULT_TS_TABLE
        else:
            translation_table = ChainMap(_DEFAULT_TS_TABLE, ts_table)
        self.translation_table = translation_table

        self._pack_table   = {}
        self._unpack_table = {}
        for code in sorted(self.translation_table):
            encoder = self.translation_table[code]
            self._pack_table[encoder.type] = (code, encoder.pack)
            self._unpack_table[code]       = encoder.unpack

    def _ext_type_pack_hook(self, obj, _sentinel=object()):
        cls = getattr(obj, '__class__')
        hit = self._pack_table.get(cls, _sentinel)

        if hit is _sentinel:
            raise TypeError("Unknown type: {!r}".format(obj))

        code, packer = hit
        return ExtType(code, packer(obj))

    def _ext_type_unpack_hook(self, code, data):
        if code not in self._unpack_table:
            raise TypeError(f"Unknown packed code: {code}")

        unpacker = self._unpack_table[code]
        # noinspection PyArgumentList
        return unpacker(data)

    def packb(self, obj) -> bytes:
        return msgpack.packb(obj, use_bin_type=True, default=self._ext_type_pack_hook)

    def unpackb(self, data: bytes):
        return msgpack.unpackb(data, use_list=False, raw=False, ext_hook=self._ext_type_unpack_hook)