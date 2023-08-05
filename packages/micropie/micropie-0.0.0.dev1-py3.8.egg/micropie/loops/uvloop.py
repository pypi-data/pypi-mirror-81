import asyncio

try:
    import uvloop
    from uvloop import __version__ as uvloop_version
except ImportError:
    uvloop_version = '0'

_UVLOOP_VERSION = '.'.join(map(str, (0,14,0)))


def uvloop_setup():
    if uvloop_version < _UVLOOP_VERSION:
        raise ImportError(f"uvloop_setup requires uvloop package (version >= {_UVLOOP_VERSION})")
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
