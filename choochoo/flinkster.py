from .base import Interface


class Flinkster(Interface):
    """Wrapper for Deutsche Bahn's Flinkster API.

    Documentation at: 
        https://developer.deutschebahn.com/store/apis/info?name=Flinkster_API_NG&version=v1&provider=DBOpenData
    """

    def __init__(self, token=None, key=None, secret=None, config=None):
        super(Flinkster, self).__init__(key=key, secret=secret, token=token,
                                        config=config)
        self.address += 'flinkster-api-ng/v1/'

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
        resp = super(Flinkster, self).request(endpoint, verb=verb, **req_kwargs)
        resp.raise_for_status()
        return resp.json()

    @staticmethod
    def _get_provider_id(provider):
        providers = {'car2go': 3, 'call-a-bike': 2, 'flinkster': 1}
        if provider.lower() not in providers:
            raise ValueError("Provider must be one of the following: 'car2go', "
                             "'call-a-bike', 'flinkster'!")
        return providers[provider]

    def get_area(self, by_id=None, provider_name=None, **endpoint_kwargs):
        """Returns search queries for areas by parameters or UUID.
        
        if by_id is passed, we're calling /areas/{uuid}, so make sure the
        endpoint_kwargs match.
        
        if it isn't passed, endpoint kwargs must be specified and at least
        provider network
        
        :param by_id: str
        :param endpoint_kwargs: supported parameters for the API
        :return: list, dict
        """
        if by_id:
            return self.request('areas/%s' % by_id, params=endpoint_kwargs)
        else:
            if 'providernetwork' not in endpoint_kwargs and not provider_name:
                raise ValueError('Must at least pass "providernetwork" as '
                                 'endpoint kwarg if no id and name are given!')
            elif provider_name:
                endpoint_kwargs['providernetwork'] = self._get_provider_id(provider_name)
            else:
                pass

            return self.request('areas', params=endpoint_kwargs)

    def booking_proposals(self, provider_name=None, **endpoint_kwargs):
        """Returns search query of bookin proposals.
        
        :param endpoint_kwargs: parameters as supported by endpoint
        :return: list, dict
        """
        if ((not all(k in endpoint_kwargs for k in ('lat', 'lon'))) or
                ('providernetwork' not in endpoint_kwargs and provider_name is None)):
            raise ValueError("Must specify kwargs 'lat', 'lon' and either"
                             "'provider_name' or 'providernetwork'")
        elif provider_name:
            endpoint_kwargs['providernetwork'] = self._get_provider_id(provider_name)

        return self.request('bookingproposals', params=endpoint_kwargs)

    def categories(self, provider, by_id=None, **endpoint_kwargs):
        """Returns available categories of specified network provider.
        
        :param provider: str, {car2go | call-a-bike | flinkster}
        :param endpoint_kwargs: supported endpoint parameters
        :return: list, dict
        """
        network_id = self._get_provider_id(provider)
        if by_id:
            return self.request('providernetworks/%s/categories/%s' %
                                (network_id, by_id), params=endpoint_kwargs)
        else:
            return self.request('providernetworks/%s/categories' % network_id,
                                params=endpoint_kwargs)

    def prices(self, provider, **endpoint_kwargs):
        """Get prices for specified Provider network.
        
        :param provider: str, {car2go | call-a-bike | flinkster}
        :param endpoint_kwargs: supported endpoint parameters
        :return: dict, list
        """
        network_id = self._get_provider_id(provider)
        return self.request('providernetworks/%s/prices' % network_id,
                            params=endpoint_kwargs)

    def rental_details(self, provider, rental_id, **endpoint_kwargs):
        """Get information about the rental object.
        
        :param provider: str, {car2go | call-a-bike | flinkster}
        :param rental_id: str
        :param endpoint_kwargs: supported endpoint parameters 
        :return: list, dict
        """
        network_id = self._get_provider_id(provider)
        return self.request('providernetworks/%s/rentalobjects/%s' %
                            (network_id, rental_id), params=endpoint_kwargs)

    def provider_details(self, provider, **endpoint_kwargs):
        """Gets details of the specified provider network.
        
        :param provider: str, {car2go | call-a-bike | flinkster}
        :param endpoint_kwargs: supported endpoint parameters 
        :return: list, dict
        """
        network_id = self._get_provider_id(provider)
        return self.request('providernetworks/%s' % network_id,
                            params=endpoint_kwargs)

    def providers(self, by_id, **endpoint_kwargs):
        """Get information about the specified  provider network resource.
                
        :param by_id: str
        :param endpoint_kwargs: supported endpoint parameters 
        :return: list, dict
        """
        return self.request('providers/%s' % by_id, params=endpoint_kwargs)