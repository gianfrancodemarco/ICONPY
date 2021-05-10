from time import sleep

from lib.queries import FILM_QUERY, create_query, ENTITY_QUERY
from lib.wikidata.wikidataAPI import WikiDataAPI
from lib.wikidata.wikimovie import WikiMovie
from lib.csvutilities import writeCSV, readCSVtoObj


def __get_uris(already_fetched=None):
    # leggiamo il csv
    data = readCSVtoObj("data/movies_lost.csv", ["id", "title"])

    # leggi da dataset with uris, trova l'ultimo id
    already_fetched = readCSVtoObj("data/dataset_with_uris.csv", ["id", "title", "uri"])

    if len(already_fetched) == 0:
        last_fetched = 0
    else:
        last_fetched = int(already_fetched[len(already_fetched) - 1]["id"])

    last_fetched = 0

    print(f'Total movies: {len(data)}')

    i = last_fetched
    for movie in data[last_fetched:]:

        print(f'Getting movie {i+1} / {len(data)}')

        # query per recupare l'uri del film
        wikidataAPI = WikiDataAPI()

        query = create_query(FILM_QUERY, [movie['title']])
        results = wikidataAPI.do_query(query)

        if results is None or len(results) == 0:
            i += 1
            continue

        result_movie = results[0]

        writeCSV(
            'data/dataset_with_uris_4000.csv',
            [[movie['id'], movie['title'], result_movie['movie']['value']]],
            mode='a'
        )

        i += 1


def get_uris():
    while True:
        try:
            __get_uris()
        except Exception as e:
            print(e)
            sleep(600)



def get_entities():
    while True:
        try:
            __get_entities()
        except Exception as e:
            print(e)
            sleep(600)


def __get_entities():
    # leggiamo il csv
    data = readCSVtoObj("data/dataset_with_uris.csv", ["id", "title", "uri"])
    data = [movie['uri'] for movie in data]
    ids = [uri.split(sep='/')[-1] for uri in data]

    print(f'Total movies: {len(ids)}')

    for i, id in enumerate(ids):

        print(f'Getting entity {i+1} / {len(ids)}')

        # query per recupare l'uri del film
        wikidataAPI = WikiDataAPI()

        query = create_query(ENTITY_QUERY, [id])
        results = wikidataAPI.do_query(query)

        wiki_movie = WikiMovie(results)
        built = wiki_movie.build()

        print(built)

