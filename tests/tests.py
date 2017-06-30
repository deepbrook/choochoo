import logging
from unittest import TestCase
from choochoo import Fahrplan, BahnPark, Cargo, FaSta, Flinkster, Reisezentren, Betriebsstellen
from requests import HTTPError
from datetime import datetime
from urllib.parse import unquote

requests_log = logging.getLogger('requests.packages.urllib3.connectionpool')
requests_log.setLevel(logging.ERROR)

class FahrplanTests(TestCase):
    def __init__(self, *args, **kwargs):
        super(FahrplanTests, self).__init__(*args, **kwargs)
        self.api = None

    def setUp(self):
        self.api = Fahrplan(config='config.ini')

    def tearDown(self):
        self.api = None

    def test_location_returns_200_and_expected_python_obj(self):
        try:
            resp = self.api.location('BERLIN')
        except HTTPError as e:
            self.fail('Status Code Was %s - URL: %s!' % (e.response.status_code, e.request.url))
        self.assertIsInstance(resp, (list, dict))

    def test_arrivals_returns_200_and_decoded_json(self):
        try:
            resp = self.api.arrivals('8011160',
                                     date=datetime.today().strftime('%Y-%m-%d'))
        except HTTPError as e:
            self.fail('Status Code Was %s - URL: %s!' % (e.response.status_code, e.request.url))
        self.assertIsInstance(resp, (list, dict))

    def test_departures_returns_200_and_decoded_json(self):
        try:
            resp = self.api.departures('8011160',
                                       date=datetime.today().strftime('%Y-%m-%d'))
        except HTTPError as e:
            self.fail('Status Code Was %s - URL: %s!' % (e.response.status_code, e.request.url))
        self.assertIsInstance(resp, (list, dict))

    def test_journey_details_returns_200_and_decoded_json(self):
        journey_id = unquote(self.api.departures('8011160')[0]['detailsId'])
        try:
            resp = self.api.journey_details(journey_id)
        except HTTPError as e:
            self.fail('Status Code Was %s - URL: %s - Journey_id: %s' %
                      (e.response.status_code, e.request.url, journey_id))
        self.assertIsInstance(resp, (list, dict))


class BahnParkTests(TestCase):
    def __init__(self, *args, **kwargs):
        super(BahnParkTests, self).__init__(*args, **kwargs)
        self.api = None

    def setUp(self):
        self.api = BahnPark(config='config.ini')

    def tearDown(self):
        self.api = None

    def test_spaces_returns_200_and_expected_python_obj(self):
        try:
            resp = self.api.spaces()
        except HTTPError as e:
            self.fail('Status Code Was %s - URL: %s!' % (e.response.status_code, e.request.url))
        self.assertIsInstance(resp, (list, dict))
        # Assert passing an ID returns data only for specified ID
        resp = self.api.spaces(by_id='100002')
        self.assertEqual(resp['id'], 100002)

    def test_pit_parking_returns_200_and_decoded_json(self):
        try:
            resp = self.api.pit_parking()
        except HTTPError as e:
            self.fail('Status Code Was %s - URL: %s!' % (e.response.status_code, e.request.url))
        self.assertIsInstance(resp, (list, dict))

    def test_occupancies_returns_200_and_decoded_json_and_supports_params(self):
        space_id = '100035'  # Bonn Hbf P1 Bonn Hbf P1 Parkhaus

        # Assert Passing no params works
        try:
            resp = self.api.occupancies()
        except HTTPError as e:
            self.fail('Status Code Was %s - URL: %s!' % (e.response.status_code, e.request.url))
        self.assertIsInstance(resp, (list, dict))

        # Assert passing an ID works
        try:
            resp = self.api.occupancies(by_id=space_id)
        except HTTPError as e:
            self.fail('Status Code Was %s - URL: %s!' % (e.response.status_code, e.request.url))
        self.assertIsInstance(resp, (list, dict))

        # Assert passing an ID and prognoses=True works
        try:
            resp = self.api.occupancies(by_id=space_id, prognoses=True)
        except HTTPError as e:
            self.fail('Status Code Was %s - URL: %s!' % (e.response.status_code, e.request.url))
        self.assertIsInstance(resp, (list, dict))

        # Assert passing prognoses=True and no ID raises a valueError
        with self.assertRaises(ValueError):
            self.api.occupancies(prognoses=True)

    def test_stations_returns_200_and_decoded_json_and_supports_params(self):
        space_id = '767'  # Bonn Hbf P1 Bonn Hbf P1 Parkhaus

        # Assert Passing no params works
        try:
            resp = self.api.stations()
        except HTTPError as e:
            self.fail('Status Code Was %s - URL: %s!' % (e.response.status_code, e.request.url))
        self.assertIsInstance(resp, (list, dict))

        # Assert passing an ID works
        try:
            resp = self.api.stations(by_id=space_id)
        except HTTPError as e:
            self.fail('Status Code Was %s - URL: %s!' % (e.response.status_code, e.request.url))
        self.assertIsInstance(resp, (list, dict))

        # Assert passing pit=True works
        try:
            resp = self.api.stations(pit=True)
        except HTTPError as e:
            self.fail('Status Code Was %s - URL: %s!' % (e.response.status_code, e.request.url))
        self.assertIsInstance(resp, (list, dict))

        # Assert passing pit=True and ID raises a valueError
        with self.assertRaises(ValueError):
            self.api.stations(by_id=space_id, pit=True)


class BetriebsstellenTests(TestCase):
    def __init__(self, *args, **kwargs):
        super(BetriebsstellenTests, self).__init__(*args, **kwargs)
        self.api = None

    def setUp(self):
        self.api = Betriebsstellen(config='config.ini')

    def tearDown(self):
        self.api = None

    def test_betriebsstellen_returns_200_and_works_as_expected(self):

        try:
            resp = self.api.betriebsstellen('Ascheberg')
        except HTTPError as e:
            self.fail('Status Code Was %s - URL: %s!' % (e.response.status_code, e.request.url))
        self.assertIsInstance(resp, (list, dict))

        try:
            resp = self.api.betriebsstellen('AAG', is_abbreviation=True)
        except HTTPError as e:
            self.fail('Status Code Was %s - URL: %s!' % (e.response.status_code, e.request.url))
        self.assertIsInstance(resp, (list, dict))


class CargoTests(TestCase):
    def __init__(self, *args, **kwargs):
        super(CargoTests, self).__init__(*args, **kwargs)
        self.api = None

    def setUp(self):
        self.api = Cargo(config='config.ini')

    def tearDown(self):
        self.api = None

    def test_betriebsstellen_returns_200_and_works_as_expected(self):
        station_id = '80007799'
        station_name = 'BERLIN-TEMPELHOF'

        try:
            resp = self.api.delays(by_name=station_name)
        except HTTPError as e:
            self.fail('Status Code Was %s - URL: %s!' % (e.response.status_code, e.request.url))
        self.assertIsInstance(resp, list)

        try:
            resp = self.api.delays(by_id=station_id)
        except HTTPError as e:
            self.fail('Status Code Was %s - URL: %s!' % (e.response.status_code, e.request.url))
        self.assertIsInstance(resp, (list, dict))

        try:
            resp = self.api.delays(by_lat_long=(52.451352, 13.409066))
        except HTTPError as e:
            self.fail('Status Code Was %s - URL: %s!' % (e.response.status_code, e.request.url))
        self.assertIsInstance(resp, (list, dict))

        # Assert theres a ValueError raised if no parameters passed
        with self.assertRaises(ValueError):
            self.api.delays()

        # Assert theres ValueError raised if more than two of the named
        # parameters are passed
        with self.assertRaises(ValueError):
            self.api.delays(by_name=station_name, by_id=station_id)


class FaStaTests(TestCase):
    def __init__(self, *args, **kwargs):
        super(FaStaTests, self).__init__(*args, **kwargs)
        self.api = None

    def setUp(self):
        self.api = FaSta(config='config.ini')

    def tearDown(self):
        self.api = None

    def test_station_facility_states_returns_200_and_expected_python_obj(self):
        station_num = 767
        try:
            resp = self.api.disruptions_by_station(station_num)
        except HTTPError as e:
            self.fail('Status Code Was %s - URL: %s!' % (e.response.status_code, e.request.url))
        self.assertIsInstance(resp, dict)

    def test_disrupted_elevators_returns_200_and_decoded_json(self):
        try:
            resp = self.api.disrupted_elevators()
        except HTTPError as e:
            self.fail('Status Code Was %s - URL: %s!' % (e.response.status_code, e.request.url))
        self.assertIsInstance(resp, (list, dict))

    def test_disrupted_escalators_returns_200_and_decoded_json(self):
        try:
            resp = self.api.disrupted_escalators()
        except HTTPError as e:
            self.fail('Status Code Was %s - URL: %s!' % (e.response.status_code, e.request.url))
        self.assertIsInstance(resp, (list, dict))

    def test_disruption_details_returns_200_and_decoded_json(self):
        disruption_num = self.api.disrupted_elevators()[0]['disruptionnumber']
        try:
            resp = self.api.disruption_details(disruption_num)
        except HTTPError as e:
            self.fail('Status Code Was %s - URL: %s!' % (e.response.status_code, e.request.url))
        self.assertIsInstance(resp, (list, dict))

    def test_get_elevators_returns_200_and_decoded_json(self):
        try:
            resp = self.api.get_elevators()
        except HTTPError as e:
            self.fail('Status Code Was %s - URL: %s!' % (e.response.status_code, e.request.url))
        self.assertIsInstance(resp, (list, dict))

    def test_get_escalators_returns_200_and_decoded_json(self):
        try:
            resp = self.api.get_escalators()
        except HTTPError as e:
            self.fail('Status Code Was %s - URL: %s!' % (e.response.status_code, e.request.url))
        self.assertIsInstance(resp, (list, dict))

    def test_facility_state_returns_200_and_decoded_json(self):
        equip_num = 10441823
        try:
            resp = self.api.facility_state(equip_num)
        except HTTPError as e:
            self.fail('Status Code Was %s - URL: %s!' % (e.response.status_code, e.request.url))
        self.assertIsInstance(resp, (list, dict))


class FlinksterTests(TestCase):
    def __init__(self, *args, **kwargs):
        super(FlinksterTests, self).__init__(*args, **kwargs)
        self.api = None

    def setUp(self):
        self.api = Flinkster(config='config.ini')

    def tearDown(self):
        self.api = None

    def test_get_area_returns_200_and_expected_python_obj(self):
        provider_network = 'flinkster'
        area_uuid = '004576141E4B6345C0E6DA9FF4162A7E24EB3855'

        # Assert searching with minimal required parameters works
        try:
            resp = self.api.get_area(provider_name=provider_network)
        except HTTPError as e:
            self.fail('Status Code Was %s - URL: %s!' % (e.response.status_code, e.request.url))
        self.assertIsInstance(resp, dict)

        # Assert searching with UUID works
        try:
            resp = self.api.get_area(by_id=area_uuid)
        except HTTPError as e:
            self.fail('Status Code Was %s - URL: %s!' % (e.response.status_code, e.request.url))
        self.assertIsInstance(resp, dict)

        # Assert passing no params raises a value error:
        with self.assertRaises(ValueError):
            self.api.get_area()

    def test_booking_proposals_returns_200_and_decoded_json(self):
        provider_network = 'flinkster'
        provider_id = 1
        lat = 52
        lon = 13

        # Assert searching with minimal required parameters works
        try:
            resp = self.api.booking_proposals(provider_name=provider_network,
                                              lat=lat, lon=lon)
        except HTTPError as e:
            self.fail('Status Code Was %s - URL: %s!' % (e.response.status_code, e.request.url))
        self.assertIsInstance(resp, dict)

        # Assert searching with providernetwork id works
        try:
            resp = self.api.booking_proposals(lon=lon, lat=lat,
                                              providernetwork=provider_id)
        except HTTPError as e:
            self.fail('Status Code Was %s - URL: %s!' % (e.response.status_code, e.request.url))
        self.assertIsInstance(resp, dict)

        # Assert passing no params raises a value error:
        with self.assertRaises(ValueError):
            self.api.booking_proposals()

        # Assert passing only lat lon raises a value Error:
        with self.assertRaises(ValueError):
            self.api.booking_proposals(lat=lat, lon=lon)

    def test_categories_returns_200_and_decoded_json(self):
        provider_id = '1'
        provider_name = 'flinkster'
        category_id  = '1000'

        # Assert querying by network only works as expected
        try:
            resp = self.api.categories(provider_name)
        except HTTPError as e:
            self.fail('Status Code Was %s - URL: %s!' % (e.response.status_code, e.request.url))
        self.assertIsInstance(resp, dict)
        self.assertIn('items', resp)

        # Assert querying by network and category ID works as expected
        try:
            resp = self.api.categories(provider_name, by_id=category_id)
        except HTTPError as e:
            self.fail('Status Code Was %s - URL: %s!' % (e.response.status_code, e.request.url))
        self.assertIsInstance(resp, (list, dict))
        self.assertNotIn('items', resp)

    def test_prices_returns_200_and_decoded_json(self):
        provider = 'flinkster'
        try:
            resp = self.api.prices(provider)
        except HTTPError as e:
            self.fail('Status Code Was %s - URL: %s!' % (e.response.status_code, e.request.url))
        self.assertIsInstance(resp, dict)

    def test_rental_details_returns_200_and_decoded_json(self):
        rental_uuid = 'Made_up_since_reference_missing'
        provider = 'flinkster'
        # Assert that request is good
        try:
            resp = self.api.rental_details(provider, rental_uuid)
        except HTTPError as e:
            self.fail('Status Code Was %s - URL: %s!' % (e.response.status_code, e.request.url))
        self.assertIsInstance(resp, dict)

    def test_provider_details_returns_200_and_decoded_json(self):
        provider = 'flinkster'
        try:
            resp = self.api.provider_details(provider)
        except HTTPError as e:
            self.fail('Status Code Was %s - URL: %s!' % (e.response.status_code, e.request.url))
        self.assertIsInstance(resp, (list, dict))

    def test_providers_returns_200_and_decoded_json(self):
        provider_network_resource = 'Made_up_since_reference_missing'
        try:
            resp = self.api.providers(provider_network_resource)
        except HTTPError as e:
            self.fail('Status Code Was %s - URL: %s!' % (e.response.status_code, e.request.url))
        self.assertIsInstance(resp, (list, dict))


class ReisezentrenTests(TestCase):
    def __init__(self, *args, **kwargs):
        super(ReisezentrenTests, self).__init__(*args, **kwargs)
        self.api = None

    def setUp(self):
        self.api = Reisezentren(config='config.ini')

    def tearDown(self):
        self.api = None

    def test_get_area_returns_200_and_expected_python_obj(self):
        center_id = '502542'
        center_name = 'Bamberg'
        lat_lon = (49.9, 10.898)
        # Assert searching with minimal required parameters works
        try:
            resp = self.api.reizentren(by_center_name=center_name)
        except HTTPError as e:
            self.fail('Status Code Was %s - URL: %s!' % (e.response.status_code, e.request.url))
        self.assertIsInstance(resp, dict)

        try:
            resp = self.api.reizentren(by_center_id=center_id)
        except HTTPError as e:
            self.fail('Status Code Was %s - URL: %s!' % (e.response.status_code, e.request.url))
        self.assertIsInstance(resp, dict)

        try:
            resp = self.api.reizentren(by_lat_lon=lat_lon)
        except HTTPError as e:
            self.fail('Status Code Was %s - URL: %s!' % (e.response.status_code, e.request.url))
        self.assertIsInstance(resp, dict)

        # Assert that a value Error is raised if no or two or more
        # named kwargs are passed
        with self.assertRaises(ValueError):
            self.api.reizentren()

        with self.assertRaises(ValueError):
            self.api.reizentren(center_id, center_name)

        with self.assertRaises(ValueError):
            self.api.reizentren(center_id, center_name, lat_lon)