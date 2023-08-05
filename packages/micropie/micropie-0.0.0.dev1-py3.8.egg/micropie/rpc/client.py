from typing import Tuple, Mapping

from micropie.lib.enums import MessageType
from micropie.lib.exceptions import ClientError
from micropie.rpc import Message
from micropie.transports.base import build_transport_from_url


# noinspection DuplicatedCode
async def rpc_client(
        service_url  : str,
        message_type : MessageType,
        method       : str,
        args         : Tuple    = None,
        kwargs       : Mapping  = None,
        timeout      : int      = None,
        ts_table     : Mapping  = None,
        send_meta    : Mapping  = None
) -> Message:

    if message_type not in (MessageType.REQUEST, MessageType.NOTIFY):
        raise ClientError(f"Invalid message type `{message_type.name}`")

    transport = build_transport_from_url(service_url, ts_table)

    if message_type == MessageType.REQUEST:
        request = transport.message_utils.build_request(method, args, kwargs, meta=send_meta)
    else:
        request = transport.message_utils.build_notify(method, args, kwargs, meta=send_meta)

    response = await transport.interchange(request, timeout=timeout)

    if request.type == MessageType.REQUEST and request.msgid != response.msgid:
        raise ClientError(f'Request/Response id mismatch {request.msgid}/{response.msgid}')

    return response
