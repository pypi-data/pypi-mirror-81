import datetime
import logging
import os
from collections import OrderedDict, defaultdict
from typing import Dict

from micropie.lib import Depends


class Registry:

    class Config:
        name = 'registry'
        desc = 'Micropie services registry'

    _registry     : OrderedDict = OrderedDict()
    _last_workers : Dict        = defaultdict(lambda : 0)

    def __init__(
            self,
            assume_offline: int = Depends(lambda: int( os.getenv('REGISTRY_ASSUME_OFFLINE', 240) ))
    ):
        self.logger = logging.getLogger('micropie.registry')
        self.assume_offline = assume_offline


    def _registry_time(self, date: datetime.datetime) -> int:
        return round(date.timestamp() * 1000)


    def _current_registry_time(self) -> int:
        return self._registry_time(date=datetime.datetime.utcnow())


    def _calc_health(self, last: int)-> float:
        health = 1 - ((self._current_registry_time() - last) / (self.assume_offline * 1000))
        health = float('%.4f' % health)
        return max(health, 0.0)


    def registrar(self, instance: str, name: str, url: str):
        self.logger.info(f'REGISTRY: {instance}/{name}')

        # registry service
        self._registry[instance] = {
            'instance': instance,
            'name': name,
            'url': url,
            'last': self._current_registry_time()
        }


    def heartbeat(self, instance: str, name: str, url: str):
        self.logger.info(f'HEARTBEAT: {instance}/{name}')

        if instance in self._registry:
            self._registry[instance]['last'] = self._current_registry_time()
        else:
            self.registrar(instance, name, url)


    # noinspection DuplicatedCode
    def lookup(self, name: str = '*', health: float = 0, instance: str = '*', sort: bool = True):
        self.logger.info(f'LOOKUP: {instance or "*"}/{name or "*"}')
        services = self._registry.values()

        # filter by name
        if (name or '*') != '*':
            services = filter(lambda s: s['name'] == name, services)
        # filter by health
        if health >= 0:
            services = filter(lambda s: self._calc_health(s['last']) >= health, services)
        # filter by instance
        if (instance or '*') != '*':
            services = filter(lambda s: s['instance'] == instance, services)

        # map properties
        worker_num = 1
        services_list = []
        for s in services:
            services_list.append({
                'instance': s['instance'],
                'worker': worker_num,
                'name': s['name'],
                'url': s['url'],
                'health': self._calc_health(s['last'])
            })
            worker_num += 1

        if sort:
            services_list = sorted(services_list, key=lambda s: s['worker'])

        return tuple(services_list)


    def get_worker(self, svc_name: str):
        services = self.lookup(name=svc_name, health=0.01)

        # reset last_worker (if necessary)
        workers = len(services)
        last_worker = self._last_workers[svc_name]
        self._last_workers[svc_name] = 0 if last_worker >= workers else last_worker

        # round-robin to select service worker
        worker = None
        for service in services:
            if service['worker'] > self._last_workers[svc_name]:
                self._last_workers[svc_name] = service['worker']
                worker = service
                break

        return worker


    def unregistry(self, instance: str):
        self.logger.info(f'UNREGISTRY: {instance}/*')
        self._registry.pop(instance, None)
