from .base import Interface


class Betriebsstellen(Interface):
    """Wrapper for Deutsche Bahn's Betriebsstellen API.

    Documentation at: 
        https://developer.deutschebahn.com/store/apis/info?name=BahnPark&version=v1&provider=DBOpenData
    """

    def __init__(self, token, key=None, secret=None, config=None):
        super(Betriebsstellen, self).__init__(key=key, secret=secret,
                                              token=token, config=config)
        self.address += 'betriebsstellen/v1/'

    def request(self, endpoint, verb=None, **req_kwargs):
        """Returns Data from BahnPark endpoint as python object.

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
        resp = super(Betriebsstellen, self).request(endpoint, verb=verb,
                                                    **req_kwargs)
        resp.raise_for_status()
        return resp.json()

    def betriebsstellen(self, station_name, is_abbreviation=False):
        """Returns data on a operation station.
        
        :param station_name: 
        :param is_abbreviation: 
        :return: 
        """
        endpoint = 'betriebsstellen'
        if is_abbreviation:
            endpoint += '/' + station_name
            return self.request(endpoint)
        else:
            return self.request(endpoint, params={'name': station_name})
