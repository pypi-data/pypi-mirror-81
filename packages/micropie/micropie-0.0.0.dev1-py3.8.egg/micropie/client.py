import asyncio
from typing import Dict

from micropie.lib.enums import MessageType, MessageMeta, SenderType
from micropie.lib.packer import Encoder
from micropie.rpc import rpc_client, rpc_proxy


class MicropieClient:

    def __init__(self, registry_url: str, registry_timeout: int = 5):
        self.registry_url = registry_url
        self.registry_timeout = registry_timeout
        self.send_meta = {
            MessageMeta.SENDER_ID: None,
            MessageMeta.SENDER_TYPE: SenderType.CLIENT,
            MessageMeta.SENDER_NAME: 'MicropieClient'
        }
        self._proxies = {}
        self._timeouts = {}
        self._ts_tables = {}

    def add_timeout(self, service: str, timeout: int):
        self._timeouts[service] = timeout
        self._proxies.pop(service, None)

    def add_ts_table(self, service: str, ts_table: Dict[int, Encoder]):
        self._ts_tables[service] = ts_table
        self._proxies.pop(service, None)

    def _get_proxy(self, service: str) -> rpc_proxy:
        if service not in self._proxies:
            proxy = rpc_proxy(service, timeout=self._timeouts.get(service), ts_table=self._ts_tables.get(service))
            proxy.configure(self.registry_url, self.registry_timeout, self.send_meta)
            self._proxies[service] = proxy

        return self._proxies[service]

    async def services(self):
        response = await rpc_client(
            service_url=self.registry_url,
            message_type=MessageType.REQUEST,
            method='lookup',
            args=('*',),
            timeout=self.registry_timeout,
            send_meta=self.send_meta
        )

        services = set( map(lambda s: s['name'], response.get_result()) )
        return tuple(services)

    async def service_info(self, service: str):
        proxy = self._get_proxy(service)

        if not proxy.timeout:
            info = await asyncio.wait_for(proxy.info(), timeout=5)
        else:
            info = await proxy.info()

        info['instances'] = await proxy.instances()
        return info

    def __getattr__(self, service):
        return self._get_proxy(service)

    __getitem__ = __getattr__
