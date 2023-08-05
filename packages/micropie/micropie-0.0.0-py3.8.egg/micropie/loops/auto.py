def auto_loop_setup():
    try:
        import uvloop
    except ImportError as exc:  # pragma: no cover
        from micropie.loops.asyncio import asyncio_setup
        asyncio_setup()

    else:
        from micropie.loops.uvloop import uvloop_setup
        uvloop_setup()
