from .base import Interface


class Reisezentren(Interface):
    """Wrapper for Deutsche Bahn's Flinkster API.

    Documentation at: 
        https://developer.deutschebahn.com/store/apis/info?name=Reisezentren&version=v1&provider=DBOpenData
    """

    def __init__(self, token=None, key=None, secret=None, config=None):
        super(Reisezentren, self).__init__(key=key, secret=secret, token=token,
                                        config=config)
        self.address += 'reisezentren/v1/'

    def request(self, endpoint, verb=None, **req_kwargs):
        """Returns Data from FaSta endpoint as python object.

        Querys API using a super() call to Interface.request(), checks the 
        HTTP status code and returns the response's json data 
        as a python object.

        :param endpoint: str
        :param verb: str
        :param req_kwargs: kwargs accepted by requests.Request() 
        :return: dict or list
        """
        req_kwargs['headers'] = {'Authorization': 'Bearer ' + self.token,
                                 'Accept': 'application/json'}
        resp = super(Reisezentren, self).request(endpoint, verb=verb, **req_kwargs)
        resp.raise_for_status()
        return resp.json()

    def reisezentren(self, by_center_name=None, by_center_id=None,
                     by_lat_lon=None, **endpoint_kwargs):
        """Get information about travel centers from the Reisezentren API.
        
        All named parameters are mutually exclusive.
        
        :param by_center_name: str, Center Name
        :param by_center_id: str, Center ID
        :param by_lat_lon: tuple, 2-float tuple describing latitude and longitude
        :param endpoint_kwargs: supported endpoint parameters
        :return: dict
        """
        c = sum([1 for v in (by_center_id, by_center_name, by_lat_lon) if v])
        if c > 1:
            raise ValueError("Named parameters are mutually exclusive! "
                             "May only pass one of them")
        elif c == 0:
            raise ValueError("Must name at least one of paramters: "
                             "by_center_name | by_center_id | by_lat_lon")
        else:

            if by_center_name:
                payload = {'name': by_center_name}
                payload.update(endpoint_kwargs)
                return self.request('reisezentren', params=payload)
            elif by_center_id:
                return self.request('reisezentren/%s' % by_center_id,
                                    params=endpoint_kwargs)
            else:
                lat, lon = by_lat_lon
                return self.request('reisezentren/loc/%s/%s' % (lat, lon),
                                    params=endpoint_kwargs)