from urllib.parse import urlparse, parse_qs, parse_qsl, urlencode


# noinspection PyMethodMayBeStatic
class Location:
    """Service location url util class"""

    _micropie_channel = 'micropie_q'

    def __init__(self, url: str):
        if not self._validate_url(url):
            raise TypeError(f"Invalid url `{url}`")

        self._parsed_url = urlparse(url=url)
        self._scheme = self._parsed_url.scheme
        self._user = self._parsed_url.username
        self._password = self._parsed_url.password
        self._host = self._parsed_url.hostname
        self._port = self._parsed_url.port
        self._path = self._parsed_url.path
        self._channel = parse_qs(self._parsed_url.query).get(self._micropie_channel, [None])[0]
        self._query = self._remove_channel()

    def _validate_url(self, url: str):
        parsed = urlparse(url=url)
        return all([parsed.scheme, parsed.netloc])

    def _remove_channel(self):
        query_params = parse_qsl(self._parsed_url.query)
        query_params = list(filter(lambda q: q[0] != self._micropie_channel, query_params))
        return urlencode(query_params)

    @property
    def scheme(self):
        return self._scheme

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port or 0

    @property
    def channel(self):
        return self._channel

    @property
    def url(self):
        return str(self)

    def update_scheme(self, scheme: str):
        self._scheme = scheme

    def update_host(self, host: str):
        self._host = host

    def update_port(self, port: int):
        self._port = port

    def update_channel(self, channel: str):
        self._channel = channel

    def __str__(self):
        url = f'{self.scheme}://'
        if self._user and self._password:
            url += f'{self._user}:{self._password}@'
        url += self._host
        if self._port:
            url += f':{self._port}'
        if self._path:
            url += f'{self._path}'
        if self._query and self._channel:
            url += f'?{self._query}&{self._micropie_channel}={self._channel}'
        elif self._channel:
            url += f'?{self._micropie_channel}={self._channel}'

        return url
