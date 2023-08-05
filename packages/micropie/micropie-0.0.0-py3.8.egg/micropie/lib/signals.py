import asyncio
import sys

from collections import defaultdict
from typing import Callable


class Signal:

    def __init__(self, name: str, signals_slots: defaultdict):
        self._name  = name
        self._slots = signals_slots[name]
        self._signals_slots = signals_slots

    @property
    def name(self):
        return self._name

    @property
    def slots(self):
        return tuple( self._slots )

    def connect(self, callback: Callable):
        self._slots.add(callback)

    def disconnect(self, callback: Callable):
        slots = set( filter(lambda x: id(x) != id(callback), self.slots) )
        self._signals_slots[self.name] = slots

    async def emit(self, *args, **kwargs):
        if not self._slots:
            print(f'Warn: Signal `{self._name}` emitted without connected slots', file=sys.stderr)

        for cb in self._slots:
            if asyncio.iscoroutinefunction(cb):
                await cb(*args, **kwargs)
            else:
                cb(*args, **kwargs)

    def emit_sync(self, *args, **kwargs):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.emit(*args, **kwargs))

    def __str__(self):
        return f"SIGNAL(name={self.name}, slots={self.slots})"


class _Signals:
    _signals_slots: defaultdict = defaultdict(set)

    def slot(self, signal: str):
        def decorator(func):
            self.signal(name=signal).connect(func)
            return func
        return decorator

    def all(self):
        return tuple( map(lambda s: self.signal(name=s), self._signals_slots.keys()) )

    def signal(self, name: str) -> Signal:
        return Signal(name=name, signals_slots=self._signals_slots)

    def disconnect(self, signal: str):
        self._signals_slots.pop(signal, None)

    def disconnect_all(self):
        self._signals_slots.clear()

    def __getattr__(self, item):
        return self.signal(name=item)

    __getitem__ = __getattr__


signals = _Signals()
