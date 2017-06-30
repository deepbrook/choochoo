from .base import Interface


class Cargo(Interface):
    """Wrapper for Deutsche Bahn's Cargo Delay Statistics API.

    Documentation at: 
        https://developer.deutschebahn.com/store/apis/info?name=Fahrplan&version=v1&provider=DBOpenData
    """

    def __init__(self, token=None, key=None, secret=None, config=None):
        super(Cargo, self).__init__(key=key, secret=secret, token=token,
                                       config=config)
        self.address += 'cargo/v1/'

    def request(self, endpoint, verb=None, **req_kwargs):
        """Returns Data from Cargo Delay Statistics endpoint as python object.

        Querys API using a super() call to Interface.request(), checks the 
        HTTP status code and returns the response's json data 
        as a python object.

        :param endpoint: str
        :param verb: str
        :param req_kwargs: kwargs accepted by requests.Request() 
        :return: Dict or list
        """
        req_kwargs['headers'] = {'Authorization': 'Bearer ' + self.token,
                                 'Accept': 'application/json'}
        resp = super(Cargo, self).request(endpoint, verb=verb, **req_kwargs)
        resp.raise_for_status()
        return resp.json()

    def delays(self, by_name=None, by_id=None, by_lat_long=None,
               **endpoint_kwargs):
        """Returns delay data available at Cargo API Endpoint.
        
        named parameters are mutually exclusive, so only one of them may evaluate
        to True at any time.
        
        :param by_name: station name
        :param by_id: station id
        :param by_lat_long: tuple, latitute and longitude
        :param endpoint_kwargs: endpoint parameters as describe in the API docs
        :return: list, dict
        """
        c = sum([1 for v in (by_name, by_id, by_lat_long) if v])
        if c > 1:
            raise ValueError("by_name, by_id and by_long_lat are "
                             "mutually exclusive!")
        if not c:
            raise ValueError("Must pass one of kwargs: by_name, by_id "
                             "and by_long_lat")
        endpoint = 'delays'
        if by_name:
            payload = {'name': by_name}
            payload.update(endpoint_kwargs)
            return self.request(endpoint, params=payload)
        elif by_id:
            endpoint += '/' + by_id
        elif by_lat_long:
            lat, long = by_lat_long
            endpoint += '/' + str(lat) + '/' + str(long)
        return self.request(endpoint, params=endpoint_kwargs)
