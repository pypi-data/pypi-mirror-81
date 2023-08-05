import functools
import typing


def _depends(callback: typing.Callable, use_cache: bool = False):
    if use_cache:
        return functools.lru_cache()(callback)()
    return callback()


Depends = _depends
