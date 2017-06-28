import datetime

from .base import Interface


class Fahrplan(Interface):
    """Wrapper for Deutsche Bahn's FahrplanPlus API.
    
    Documentation at: 
        https://developer.deutschebahn.com/store/apis/info?name=Fahrplan&version=v1&provider=DBOpenData
    """
    def __init__(self, token, key=None, secret=None, config=None):
        super(Fahrplan, self).__init__(key=key, secret=secret, token=token,
                                           config=config)
        self.address += 'fahrplan-plus/v1/'

    def request(self, endpoint, verb=None, **req_kwargs):
        """Returns Data from FahrplanPlus endpoint as python object.
        
        Querys API using a super() call to Interface.request(), checks the 
        HTTP status code and returns the response's json data 
        as a python object.
        
        :param endpoint: str
        :param verb: str
        :param req_kwargs: kwargs accepted by requests.Request() 
        :return: Dict or list
        """
        req_kwargs['headers'] = {'Authorization': 'Bearer '+self.token,
                                 'Accept': 'application/json'}
        resp = super(Fahrplan, self).request(endpoint, verb=verb,
                                                 **req_kwargs)
        resp.raise_for_status()
        return resp.json()

    def location(self, location_name):
        """Get locations that match the given string
        
        :param location_name: str
        :return: requests.Response()
        """
        return self.request('location/%s' % location_name)

    def arrivals(self, location_id, date=None):
        """Returns arrivals of given location and date.
        
        :param location_id: str
        :param date: date as string in format YYYY-MM-DD
        :return: requests.Response()
        """
        return self.request('arrivalBoard/%s' % location_id,
                            params={'data': date})

    def departures(self, location_id, date=None):
        """Returns departures of given location and date.

        :param location_id: str
        :param date: date as string in format YYYY-MM-DD
        :return: requests.Response()
        """
        date = datetime.datetime.today().strftime('%Y-%m-%d') if not date else date
        return self.request('departuresBoard/%s' % location_id,
                            params={'data': date})

    def journey_details(self, journey_id):
        """Returns details for given journey's id.
        
        :param journey_id: str
        :return: requests.Response()
        """
        return self.request('journeyDetails/%s' % journey_id)
