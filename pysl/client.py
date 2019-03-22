import urllib3
import certifi
import json
from pysl import resources
from pysl.exceptions import (APINotInitializedError,
                             APIKeyUndefinedError,
                             APIKeyInvalidError,
                             APIUnavailableError)

class SLClient:
    def __init__(self,
                 type_ahead_key: str = None,
                 realtime_departures_key: str = None,
                 server_addr: str = 'https://api.sl.se'):
        self._server_addr = server_addr
        self._type_ahead_api: TypeAheadAPI = None
        self._realtime_departures_api: RealtimeDeparturesAPI = None

        if type_ahead_key:
            self.init_type_ahead(type_ahead_key)

        if realtime_departures_key:
            self.init_realtime_departures(realtime_departures_key)

    def type_ahead(self, search_string):
        if self._type_ahead_api is None:
            raise APINotInitializedError('TypeAheadAPI not yet initialized.')
        return self._type_ahead_api.search(search_string)

    def realtime_departures(self, stop_id, time_window):
        if self._realtime_departures_api is None:
            raise APINotInitializedError('RealtimeDeparturesAPI not yet initialized.')
        return self._realtime_departures_api.search(stop_id, time_window)

    def init_type_ahead(self, api_key):
        self._type_ahead_api = TypeAheadAPI(self._server_addr, api_key)

    def init_realtime_departures(self, api_key):
        self._realtime_departures_api = RealtimeDeparturesAPI(self._server_addr,
                                                              api_key)


class BaseAPI:
    """ Base class for all SL APIs """
    URL_TEMPLATE: str = '{server}/api2/{endpoint}.json?{request_args}'

    def __init__(self, server: str, api_key: str, data_objects: list = []):
        self._server = server
        self._options = dict(key=api_key)
        self._http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
        self._raw = None
        self._data_objects = [resources.general.ResponseEnvelope] + data_objects

    def _hook(self, dct):
        for data_object in self._data_objects:
            if set(data_object.__annotations__).issuperset(set(dct)):
                return data_object(**dct)

        return dct

    def _get_url(self, extra_options: dict) -> str:
        options = {**self._options, **extra_options}
        request_args = urllib3.request.urlencode(options)
        return self.URL_TEMPLATE.format(server=self._server,
                                        endpoint=self.ENDPOINT,
                                        request_args=request_args)

    def _make_request(self, http_method='GET', **query):
        filtered_query = {k: v for k, v in query.items() if v is not None}
        url = self._get_url(filtered_query)
        request = self._http.request(http_method, url)
        data = json.loads(request.data, object_hook=self._hook)

        if data.StatusCode == 0:
            return data
        if data.StatusCode == 1001:
            raise APIKeyUndefinedError(data.Message)
        if data.StatusCode == 1002:
            raise APIKeyInvalidError(data.Message)
        if data.StatusCode == 1003:
            raise APIUnavailableError(data.Message)


class TypeAheadAPI(BaseAPI):
    ENDPOINT: str = 'typeahead'
    def __init__(self, server: str, api_key: str):
        super().__init__(server, api_key, resources.type_ahead.__all__)

    def search(self,
               search_string: str,
               stations_only: bool = None,
               max_results: int = None,
               site_type: str = None):
        results = self._make_request(SearchString=search_string,
                                     StationsOnly=stations_only,
                                     MaxResults=max_results,
                                     Type=site_type)

        return results


class RealtimeDeparturesAPI(BaseAPI):
    ENDPOINT: str = 'realtimedeparturesV4'
    def __init__(self, server: str, api_key: str):
        super().__init__(server, api_key, resources.realtime_departures.__all__)

    def search(self,
               site_id: int,
               time_window: int,
               include_bus: bool = None,
               include_metro: bool = None,
               include_train: bool = None,
               include_tram: bool = None,
               include_ship: bool = None):

        results = self._make_request(SiteId=site_id,
                                     TimeWindow=time_window,
                                     Bus=include_bus,
                                     Metro=include_metro,
                                     Train=include_train,
                                     Tram=include_tram,
                                     Ship=include_ship)
        return results
