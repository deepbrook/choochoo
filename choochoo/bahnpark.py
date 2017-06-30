from .base import Interface


class BahnPark(Interface):
    """Wrapper for Deutsche Bahn's BahnPark API.

    Documentation at: 
        https://developer.deutschebahn.com/store/apis/info?name=BahnPark&version=v1&provider=DBOpenData
    """

    def __init__(self, token=None, key=None, secret=None, config=None):
        super(BahnPark, self).__init__(key=key, secret=secret, token=token,
                                       config=config)
        self.address += 'bahnpark/v1/'

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
                                 'Accept': 'application/json;charset=utf-8'}
        resp = super(BahnPark, self).request(endpoint, verb=verb,
                                             **req_kwargs)
        resp.raise_for_status()
        return resp.json()

    def spaces(self, by_id=None, by_name=None, **endpoint_kwargs):
        """Get available parking spaces at given location.
        
        If no id or name is given, returns a list of all parking spaces.

        :param by_id: str, ID of the space you want to know more about
        :param by_id: str, Name of the station you want to know more about
        :param endpoint_kwargs: optional parameters of the endpoint
        :return: dict
        """
        if (by_id and by_name):
            raise ValueError("Must specify only one station name or "
                             "location ID!")

        if by_name:
            payload = {'name': by_name}
            payload.update(endpoint_kwargs)
            return self.request('spaces', params=payload)
        elif by_id:
            return self.request('spaces/' + by_id, params=endpoint_kwargs)
        else:
            return self.request('spaces', params=endpoint_kwargs)

    def pit_parking(self, **endpoint_kwargs):
        """Retrieves a list of locations for pit parking services.

        including pricing and available spaces etc.

        :param endpoint_kwargs: optional parameters of the endpoint
        :return: dict
        """
        return self.request('spaces/pit', params=endpoint_kwargs)

    def occupancies(self, by_id=None, prognoses=False):
        """Return Occupancy data from BahnPark
        
        :param by_id: str, ID of space you want data on
        :param prognoses: return prognoses for given ID, if available
        :return: dict, list
        """
        if prognoses and not by_id:
            raise ValueError("Must specify a space ID to get prognoses")

        endpoint = 'spaces'
        if by_id:
            endpoint = 'spaces/%s' % by_id
            if prognoses:
                endpoint += '/prognoses'
            else:
                endpoint += '/occupancies'
        else:
            endpoint += '/occupancies'

        return self.request(endpoint)

    def stations(self, by_id=None, pit=False):
        """Query managing station data available at BahnPark.
        
        Must choose between by_id or pit=True, since they are mutually exclusive.
        
        :param by_id: str, ID of a station
        :param pit: bool, request data specific to PIT parking 
        :return: dict, list
        """
        if pit and by_id:
            raise ValueError("stations/pit doesn't support querying by ID! "
                             "Must choose either!")

        endpoint = 'stations'
        if pit:
            endpoint += '/pit'
        elif by_id:
            endpoint += '/' + by_id

        return self.request(endpoint)

