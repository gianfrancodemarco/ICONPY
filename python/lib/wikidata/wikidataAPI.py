import time

import requests

STD_ENDPOINT = "https://query.wikidata.org/sparql"
HEADERS = {"User-Agent": "icon-bot/1.0"}


class WikiDataAPI:

    def __init__(self, endpoint=STD_ENDPOINT, debug=False):
        self.endpoint = endpoint
        self.debug = debug

    def do_query(self, params):

        if params['query'] is None:
            raise Exception("Query param is mandatory")

        self._log(f'Quering {self.endpoint} at {time.ctime(time.time())}')
        self._log(f'Query: {params["query"]}')

        start = time.time()
        result = requests.get(self.endpoint, params, headers=HEADERS)
        end = time.time()
        self._log(f'Elapsed: {end - start}s')

        try:
            parsed = result.json()
        except Exception:
            print('Error in request')
            print(result.content)
            return

        parsed = parsed['results']['bindings']
        return parsed

    def get_resource(self, uri):

        self._log(f'Quering {uri}')

        start = time.time()
        result = requests.get(self.endpoint, {"format": "json"}, headers=HEADERS)
        end = time.time()
        self._log(f'Elapsed: {end - start}s')

        try:
            parsed = result.json()
        except Exception as e:
            print('Error in request')
            print(e)
            print(result.content)
            return

        parsed = parsed['results']['bindings']
        return parsed

    def _log(self, log):
        if self.debug:
            print(log)
