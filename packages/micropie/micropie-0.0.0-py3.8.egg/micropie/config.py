import logging
import sys

from micropie.lib import Location, importer

LOOP_SETUPS = {
    "auto"   : "micropie.loops.auto:auto_loop_setup",
    "asyncio": "micropie.loops.asyncio:asyncio_setup",
    "uvloop" : "micropie.loops.uvloop:uvloop_setup",
}

TRANSPORTS = {
    'tcp'  : 'micropie.transports.tcp:TcpTransport',
    'redis': 'micropie.transports.redis:RedisTransport',
    'amqp' : 'micropie.transports.amqp:AmqpTransport'
}

LOG_LEVELS = {
    "critical": logging.CRITICAL,
    "error"   : logging.ERROR,
    "warning" : logging.WARNING,
    "info"    : logging.INFO,
    "debug"   : logging.DEBUG,
}


def get_logger(log_level, log_handlers: list = None):
    if isinstance(log_level, str):
        log_level = LOG_LEVELS[log_level]
    logging.basicConfig(format="%(asctime)s (%(name)s) [%(levelname)s]: %(message)s", level=log_level)
    logger = logging.getLogger("micropie.service")
    logger.setLevel(log_level)
    for hdlr in log_handlers or []:
        logger.addHandler(hdlr)
    return logger


class Config:
    def __init__(
            self,
            cls,
            loop             : str = 'auto',
            transport_url    : str = 'tcp://0.0.0.0',
            registry_url     : str = None,
            registry_timeout : int = 5,
            heartbeats_delay : int = 120,
            log_level        : str = 'info'
    ):
        # cmd line configs
        self.cls              = cls
        self.loop             = loop
        self.transport_url    = transport_url
        self.registry_url     = registry_url
        self.registry_timeout = registry_timeout
        self.heartbeats_delay = heartbeats_delay
        self.log_level        = log_level

        # loaded classes
        self.loaded_service_cls   = None
        self.loaded_transport_cls = None

        # service level configs (Service.Config class)
        self.name         = None
        self.desc         = ''
        self.log_handlers = []
        self.ts_table     = None

        # internal attrs
        self._logger = None
        self.loaded  = False

    # noinspection DuplicatedCode
    def load(self):
        assert not self.loaded
        try:
            if isinstance(self.cls, type):
                self.loaded_service_cls = self.cls
            elif isinstance(self.cls, str):
                self.loaded_service_cls = importer.import_from_string(self.cls)
            else:
                self.logger_instance.error("Invalid cls param, must be either str or type.")
                sys.exit(1)
        except importer.ImportFromStringError as e:
            self.logger_instance.error("Loading Service class. %s" % e)
            sys.exit(1)

        try:
            self.loaded_transport_cls = importer.import_from_string( TRANSPORTS[Location(self.transport_url).scheme] )
        except importer.ImportFromStringError as e:
            self.logger_instance.error("Error loading Transport class. %s" % e)
            sys.exit(1)

        loaded_config_cls = getattr(self.loaded_service_cls, 'Config', None)
        if loaded_config_cls:
            self.name = getattr(loaded_config_cls, 'name', None)
            self.desc = getattr(loaded_config_cls, 'desc', '')
            self.log_handlers = getattr(loaded_config_cls, 'log_handlers', [])
            self.ts_table = getattr(loaded_config_cls, 'ts_table', None)

        self.name = self.name or getattr(self.loaded_service_cls, '__name__').lower()
        self.loaded = True

    def setup_event_loop(self):
        loop_setup = importer.import_from_string( LOOP_SETUPS[self.loop] )
        loop_setup()

    @property
    def logger_instance(self):
        if self._logger is None:
            self._logger = get_logger(self.log_level, self.log_handlers)
        return self._logger
