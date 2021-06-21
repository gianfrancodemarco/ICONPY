import logging
import time

import requests

STD_ENDPOINT = "https://query.wikidata.org/sparql"
HEADERS = {"User-Agent": "icon-bot/1.0"}


def do_query(params):

    if params['query'] is None:
        raise Exception("Query param is mandatory")

    logging.debug(f'Quering {STD_ENDPOINT} at {time.ctime(time.time())}')
    logging.debug(f'Query: {params["query"]}')

    start = time.time()
    result = requests.get(STD_ENDPOINT, params, headers=HEADERS)
    end = time.time()
    logging.debug(f'Elapsed: {end - start}s')

    try:
        parsed = result.json()
    except Exception:
        print('Error in request')
        print(result.content)
        return

    parsed = parsed['results']['bindings']
    return parsed


def get_resource(uri):
    logging.debug(f'Quering {uri}')

    start = time.time()
    result = requests.get(STD_ENDPOINT, {"format": "json"}, headers=HEADERS)
    end = time.time()
    logging.debug(f'Elapsed: {end - start}s')

    try:
        parsed = result.json()
    except Exception as e:
        logging.error('Error in request')
        logging.error(e)
        logging.error(result.content)
        return

    parsed = parsed['results']['bindings']
    return parsed
