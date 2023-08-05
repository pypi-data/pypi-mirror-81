from enum import Enum


class MessageType(Enum):
    REQUEST = 0
    RESPONSE = 1
    NOTIFY = 2

    def __repr__(self):
        return self.name


class ResultType(Enum):
    SINGLE_RESULT = 0
    STREAM_RESULT = 1
    ERROR_RESULT = 2

    def __repr__(self):
        return self.name


class MessageMeta(str, Enum):
    MESSAGE_TYPE = 'MESSAGE_TYPE'
    MESSAGE_ID = 'MESSAGE_ID'
    SERVER = 'SERVER'  #
    SERVER_VERSION = 'SERVER_VERSION'  #
    CLIENT = 'CLIENT'  #
    CLIENT_VERSION = 'CLIENT_VERSION'  #
    ISSUE_DATETIME = 'ISSUE_DATETIME'
    FEEDBACK_TO = 'FEEDBACK_TO'
    SERVICE = 'SERVICE'  #
    INSTANCE = 'INSTANCE'  #
    RESULT_TYPE = 'RESULT_TYPE'
    STREAM_ID = 'STREAM_ID'
    STREAM_WORKER_URL = 'STREAM_WORKER_URL'
    STREAM_HAS_NEXT = 'STREAM_HAS_NEXT'

    # nuevas
    MICROPIE_VERSION = 'MICROPIE_VERSION'
    SENDER_TYPE = 'SENDER_TYPE'
    SENDER_ID = 'SENDER_ID'
    SENDER_NAME = 'SENDER_NAME'

    def __repr__(self):
        return self.name


class SenderType(str, Enum):
    SERVICE = 'SERVICE'
    CLIENT = 'SERVICE'

    def __repr__(self):
        return self.name


class ServerFunction(str, Enum):
    INFO = '_micropie.server.info'
    PING = '_micropie.server.ping'
    STREAM_NEXT = '_micropie.server.stream.next'

    def __repr__(self):
        return self.name
