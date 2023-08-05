import inspect
import typing


class Stream:
    _sentinel = object()

    @classmethod
    def can_stream(cls, obj) -> bool:
        return inspect.isgenerator(obj) or inspect.isasyncgen(obj)

    @classmethod
    def create_stream(cls, obj: typing.Union[typing.Generator, typing.AsyncGenerator]) -> 'Stream':
        return cls(generator=obj)

    def __init__(self, generator):
        if not self.can_stream(generator):
            raise TypeError('Can not stream from: {!r}'.format(generator))

        self.__generator = generator
        next_func_name = '__anext__' if inspect.isasyncgen(generator) else '__next__'
        self._next_func = getattr(generator, next_func_name)
        self._next_value = self._sentinel
        self._has_next = self._sentinel

    async def _call_next(self):
        if inspect.isasyncgen(self.__generator):
            return await self._next_func()
        return self._next_func()

    @property
    async def has_next(self):
        if self._has_next is self._sentinel:
            # noinspection PyBroadException
            try:
                self._next_value = await self._call_next()
            except Exception:
                self._next_value = self._sentinel
            self._has_next = self._next_value is not self._sentinel
        return self._has_next


    async def next(self):
        if self._next_value is not self._sentinel:
            result = self._next_value
            self._next_value = self._sentinel
            return result

        self._has_next = self._sentinel
        try:
            return await self._call_next()
        except Exception:
            raise StopAsyncIteration from None
