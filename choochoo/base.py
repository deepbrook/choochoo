import requests
import configparser

class Interface:
    def __init__(self, *, key, secret, token, config=None):
        self.key = key
        self.secret = secret
        self.token = token
        self.address = 'https://api.deutschebahn.com/'
        if config:
            self.load_config(config)

    def load_config(self, path):
        parser = configparser.ConfigParser()
        parser.read(path)
        try:
            self.key = parser['AUTH']['key']
        except KeyError:
            print("No consumer key found in config!")

        try:
            self.secret = parser['AUTH']['secret']
        except KeyError:
            print("No consumer secret found in config!")

        try:
            self.token = parser['AUTH']['token']
        except KeyError:
            print("No access token found in config!")

    def generate_url(self, endpoint):
        return self.address + endpoint

    def request(self, endpoint, verb=None, **req_kwargs):
        verb = 'GET' if not verb else verb
        url = self.generate_url(endpoint)
        return requests.request(verb, url, **req_kwargs)