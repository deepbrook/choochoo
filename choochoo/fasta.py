from .base import Interface


class FaSta(Interface):
    """Wrapper for Deutsche Bahn's FaSta API.

    Documentation at: 
        https://developer.deutschebahn.com/store/apis/info?name=FaSta-Station_Facilities_Status&version=v1&provider=DBOpenData
    """

    def __init__(self, token=None, key=None, secret=None, config=None):
        super(FaSta, self).__init__(key=key, secret=secret, token=token,
                                    config=config)
        self.address += 'fasta/v1/'

    def request(self, endpoint, verb=None, **req_kwargs):
        """Returns Data from FaSta endpoint as python object.

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
        resp = super(FaSta, self).request(endpoint, verb=verb, **req_kwargs)
        resp.raise_for_status()
        return resp.json()

    def disruptions_by_station(self, station_number, **endpoint_kwargs):
        """Return infromation about discruptions at given station by id.
        
        :param station_number: str, station number
        :return: 
        """
        return self.request('stations/%s' % station_number,
                            params=endpoint_kwargs)

    def disrupted_elevators(self, **endpoint__kwargs):
        """Returns data on disrupted elevators.
        
        :param endpoint__kwargs: parameters as accepted by the API endpoint
        :return: 
        """
        return self._disruptions('ELEVATOR', **endpoint__kwargs)

    def disrupted_escalators(self, **endpoint_kwargs):
        """Returns data on disrupted escalators.

        :param endpoint__kwargs: parameters as accepted by the API endpoint
        :return: 
        """
        return self._disruptions('ESCALATOR', **endpoint_kwargs)

    def _disruptions(self, type, **endpoint_kwargs):
        payload = {'type': type}
        payload.update(endpoint_kwargs)
        return self.request('disruptions', params=payload)

    def disruption_details(self, disruption_num, **endpoint_kwargs):
        """Queries details about the specified disruption number.
        
        :param disruption_num: str
        :param endpoint_kwargs: parameters as accepted by the API endpoint
        :return: 
        """
        return self.request('disruptions/%s' % disruption_num,
                            params=endpoint_kwargs)

    def get_elevators(self, active=False, **endpoint_kwargs):
        """Get details on elevators.
        
        :param active: bool, whether to return active or inactive elevators
        :param endpoint_kwargs: parameters as accepted by the API endpoint
        :return: 
        """
        return self._facilities('ELEVATOR', active, **endpoint_kwargs)

    def get_escalators(self, active=False, **endpoint_kwargs):
        """Get details on escalators.

        :param active: bool, whether to return active or inactive escalators
        :param endpoint_kwargs: parameters as accepted by the API endpoint
        :return: 
        """
        return self._facilities('ESCALATOR', active, **endpoint_kwargs)

    def _facilities(self, fac_type, active, **endpoint_kwargs):
        state = 'ACTIVE' if active else 'INACTIVE'
        payload = {'type': fac_type, 'state': state}
        payload.update(endpoint_kwargs)
        return self.request('facilities', params=payload)

    def facility_state(self, equip_num, **endpoint_kwargs):
        """Returns information about the facility's state.
        
        :param equip_num: str
        :param endpoint_kwargs: parameters as accepted by the API endpoint
        :return: 
        """
        return self.request('facilities/%s' % equip_num, params=endpoint_kwargs)
