import requests
import time

STD_ENDPOINT = "https://query.wikidata.org/sparql"


class WikiDataAPI:

    def __init__(self, endpoint=STD_ENDPOINT):
        self.endpoint = endpoint

    def do_query(self, params):

        if params['query'] is None:
            raise Exception("Query param is mandatory")

        print(f'Quering {self.endpoint} at {time.ctime(time.time())}')
        #print(f'Query: {params["query"]}')

        start = time.time()
        result = requests.get(self.endpoint, params)
        end = time.time()
        print(f'Elapsed: {end - start}s')

        try:
            parsed = result.json()
        except Exception:
            print('Error in request')
            print(result.content)
            return

        parsed = parsed['results']['bindings']
        return parsed

    def get_resource(self, uri):

        print(f'Quering {uri}')

        start = time.time()
        result = requests.get(self.endpoint, {"format": "json"})
        end = time.time()
        print(f'Elapsed: {end - start}s')

        try:
            parsed = result.json()
        except Exception as e:
            print('Error in request')
            print(e)
            print(result.content)
            return

        parsed = parsed['results']['bindings']
        return parsed
