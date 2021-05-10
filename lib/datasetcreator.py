from time import sleep

from lib.queries import FILM_QUERY, create_query, ENTITY_QUERY
from lib.wikidata.wikidataAPI import WikiDataAPI
from lib.wikidata.wikimovie import WikiMovie
from lib.csvutilities import writeCSV, readCSVtoObj
import webbrowser



def get_uris():
    while True:
        try:
            __get_uris()
        except Exception as e:
            print(e)
            sleep(600)


def __get_uris(resume_id=0):

    # leggiamo il csv
    data = readCSVtoObj("data/dataset.csv", ["id", "title"])

    print(f'Total movies: {len(data)}')

    wikidataAPI = WikiDataAPI()

    for i, movie in data[resume_id:]:

        print(f'Getting movie {i+1} / {len(data)}')

        query = create_query(FILM_QUERY, [movie['title']])
        results = wikidataAPI.do_query(query)

        if (results is not None) and len(results) > 0:
            result_movie = results[0]

            writeCSV(
                'data/dataset_with_uris_4000.csv',
                [[movie['id'], movie['title'], result_movie['movie']['value']]],
                mode='a'
            )


def get_entities(resume_id=0, ids_list=None):
    while True:
        try:
            __get_entities(resume_id, ids_list)
        except Exception as e:
            print(e)
            sleep(600)


def __get_entities(resume_id=0, ids_list=None):

    if ids_list is not None: #se passo una lista di id, recupero quelli
        ids = ids_list
    else: #altrimenti li recupero dal csv
        # leggiamo il csv
        data = readCSVtoObj("data/_old_dataset_with_uris.csv", ["id", "title", "uri"])
        data = [movie['uri'] for movie in data]
        ids = [uri.split(sep='/')[-1] for uri in data]

    print(f'Total movies: {len(ids)}')

    wikidataAPI = WikiDataAPI(debug=False)

    for i, idx in enumerate(ids[resume_id:]):

        print(f'Getting entity {i+resume_id+1} / {len(ids)}')

        query = create_query(ENTITY_QUERY, [idx])
        results = wikidataAPI.do_query(query)

        wiki_movie = WikiMovie(results)
        wiki_movie.build_full()
        wiki_movie.set_prop("wiki_data_id", idx)

        try:
            wiki_movie.serialize()
        except KeyError as e:
            chrome_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
            webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
            webbrowser.get("chrome").open(f"https://www.wikidata.org/wiki/{idx}")
            print(f'Error on movie: {idx}')
            print(e)
            input()

