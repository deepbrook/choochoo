from unittest import TestCase
from choochoo import Fahrplan, BahnPark, Cargo
from requests import HTTPError


class FahrplanPlusTests(TestCase):
    def __init__(self, *args, **kwargs):
        super(FahrplanPlusTests, self).__init__(*args, **kwargs)
        self.api = None

    def setUp(self):
        self.api = Fahrplan(config='config.ini')

    def tearDown(self):
        self.api = None

    def test_location_returns_200_and_expected_python_obj(self):
        try:
            resp = self.api.location('BERLIN')
        except HTTPError:
            self.fail('Status Code Was NOT 200!')
        self.assertIsInstance(resp, (list, dict))

    def test_arrivals_returns_200_and_decoded_json(self):
        try:
            resp = self.api.arrivals('8011160')
        except HTTPError:
            self.fail('Status Code Was NOT 200!')
        self.assertIsInstance(resp, (list, dict))

    def test_departures_returns_200_and_decoded_json(self):
        try:
            resp = self.api.departures('8011160')
        except HTTPError:
            self.fail('Status Code Was NOT 200!')
        self.assertIsInstance(resp, (list, dict))

    def test_journey_details_returns_200_and_decoded_json(self):
        journey_id = '188058%2F75060%2F783144%2F328886%2F80%3fstation_evaId%3D8011160'
        try:
            resp = self.api.journey_details(journey_id)
        except HTTPError:
            self.fail('Status Code Was NOT 200!')
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
        except HTTPError:
            self.fail('Status Code Was NOT 200!')
        self.assertIsInstance(resp, (list, dict))
        # Assert passing an ID returns data only for specified ID
        resp = self.api.spaces(by_id=100002)
        self.assertEqual(resp['id'], 100002)

    def test_pit_parking_returns_200_and_decoded_json(self):
        try:
            resp = self.api.arrivals('8011160')
        except HTTPError:
            self.fail('Status Code Was NOT 200!')
        self.assertIsInstance(resp, (list, dict))

    def test_occupancies_returns_200_and_decoded_json_and_supports_params(self):
        space_id = '100035'  # Bonn Hbf P1 Bonn Hbf P1 Parkhaus

        # Assert Passing no params works
        try:
            resp = self.api.occupancies()
        except HTTPError:
            self.fail('Status Code Was NOT 200!')
        self.assertIsInstance(resp, (list, dict))

        # Assert passing an ID works
        try:
            resp = self.api.occupancies(by_id=space_id)
        except HTTPError:
            self.fail('Status Code Was NOT 200!')
        self.assertIsInstance(resp, (list, dict))

        # Assert passing an ID and prognoses=True works
        try:
            resp = self.api.occupancies(by_id=space_id, prognoses=True)
        except HTTPError:
            self.fail('Status Code Was NOT 200!')
        self.assertIsInstance(resp, (list, dict))

        # Assert passing prognoses=True and no ID raises a valueError
        with self.assertRaises(ValueError):
            self.api.occupancies(prognoses=True)

    def test_stations_returns_200_and_decoded_json_and_supports_params(self):
        space_id = '100035'  # Bonn Hbf P1 Bonn Hbf P1 Parkhaus

        # Assert Passing no params works
        try:
            resp = self.api.stations()
        except HTTPError:
            self.fail('Status Code Was NOT 200!')
        self.assertIsInstance(resp, (list, dict))

        # Assert passing an ID works
        try:
            resp = self.api.stations(by_id=space_id)
        except HTTPError:
            self.fail('Status Code Was NOT 200!')
        self.assertIsInstance(resp, (list, dict))

        # Assert passing pit=True works
        try:
            resp = self.api.stations(pit=True)
        except HTTPError:
            self.fail('Status Code Was NOT 200!')
        self.assertIsInstance(resp, (list, dict))

        # Assert passing pit=True and ID raises a valueError
        with self.assertRaises(ValueError):
            self.api.stations(by_id=space_id, prognoses=True)


class BetriebsstellenTests(TestCase):
    def __init__(self, *args, **kwargs):
        super(BetriebsstellenTests, self).__init__(*args, **kwargs)
        self.api = None

    def setUp(self):
        self.api = BahnPark(config='config.ini')

    def tearDown(self):
        self.api = None

    def test_betriebsstellen_returns_200_and_works_as_expected(self):
        try:
            resp = self.api.betriebsstellen()
        except HTTPError:
            self.fail('Status Code Was NOT 200!')
        self.assertIsInstance(resp, list)

        try:
            resp = self.api.betriebsstellen('Ascheberg')
        except HTTPError:
            self.fail('Status Code Was NOT 200!')
        self.assertIsInstance(resp, (list, dict))

        try:
            resp = self.api.betriebsstellen('AAG', is_abbreviation=True)
        except HTTPError:
            self.fail('Status Code Was NOT 200!')
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
        except HTTPError:
            self.fail('Status Code Was NOT 200!')
        self.assertIsInstance(resp, list)

        try:
            resp = self.api.delays(by_id=station_id)
        except HTTPError:
            self.fail('Status Code Was NOT 200!')
        self.assertIsInstance(resp, (list, dict))

        try:
            resp = self.api.delays(by_lat_long=(52.451352, 13.409066))
        except HTTPError:
            self.fail('Status Code Was NOT 200!')
        self.assertIsInstance(resp, (list, dict))

        # Assert theres a ValueError raised if no parameters passed
        with self.assertRaises(ValueError):
            self.api.delays()

        # Assert theres ValueError raised if more than two of the named
        # parameters are passed
        with self.assertRaises(ValueError):
            self.api.delays(by_name=station_name, by_id=station_id)
