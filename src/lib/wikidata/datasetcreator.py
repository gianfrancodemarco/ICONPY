from time import sleep

import webbrowser

from src.lib.omdbapi.omdbapi import OMDBApi
from src.lib.utils.csvutils import writeCSV, readCSVtoObj
from src.lib.utils.queryutils import create_query, FILM_QUERY, ENTITY_QUERY
from src.lib.utils.serializeutils import deserialize, serialize
from src.lib.utils.utils import all_files_in_path
from src.lib.wikidata.wikidataAPI import WikiDataAPI
from src.lib.wikidata.wikimovie import WikiMovie, WIKI_MOVIE_PROPS

PATH_SERIALIZED_FULL = "resources/data/serialized_movies_full/"
PATH_SERIALIZED = "resources/data/serialized_movies/"
PATH_SERIALIZED_IMDB = "resources/data/serialized_movies_with_imdb_score/"
FULL_CSV_PATH = "resources/data/movies.csv"


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

        print(f'Getting movie {i + 1} / {len(data)}')

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
    if ids_list is not None:  # se passo una lista di id, recupero quelli
        ids = ids_list
    else:  # altrimenti li recupero dal csv
        # leggiamo il csv
        data = readCSVtoObj("data/_old_dataset_with_uris.csv", ["id", "title", "uri"])
        data = [movie['uri'] for movie in data]
        ids = [uri.split(sep='/')[-1] for uri in data]

    print(f'Total movies: {len(ids)}')

    wikidataAPI = WikiDataAPI(debug=False)

    for i, idx in enumerate(ids[resume_id:]):

        print(f'Getting entity {i + resume_id + 1} / {len(ids)}')

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


def serialize_movies():
    file_names = all_files_in_path(PATH_SERIALIZED_FULL)

    for i, file in enumerate(file_names):
        print(f"Deserializing: {i + 1}/{len(file_names)}")
        movie = deserialize(PATH_SERIALIZED_FULL + file)
        movie.build()
        serialize(movie, PATH_SERIALIZED + file)


def serialize_movies_with_imdb_score():
    already_serialized = all_files_in_path(PATH_SERIALIZED_IMDB)
    to_serialize = all_files_in_path(PATH_SERIALIZED)
    to_serialize = [movie for movie in to_serialize if movie not in already_serialized]
    omdbapi = OMDBApi()

    for i, file in enumerate(to_serialize):
        print(f"Deserializing: {i + 1}/{len(to_serialize)}")
        movie = deserialize(PATH_SERIALIZED + file)

        if "IMDb_ID" in movie.props:

            if type(movie.props['IMDb_ID']) == list:
                id = movie.props['IMDb_ID'][0]['value']
            else:
                id = movie.props['IMDb_ID']['value']

            result = omdbapi.get_movie(id).json()

            movie.set_prop("metascore", result["Metascore"])
            movie.set_prop("imdbRating", result["imdbRating"])
            movie.set_prop("imdbVotes", result["imdbVotes"])

        movie.build()
        serialize(movie, PATH_SERIALIZED_IMDB + file)


def create_full_csv():
    lines = []
    to_insert = all_files_in_path(PATH_SERIALIZED_IMDB)

    for filename in to_insert:
        movie = deserialize(PATH_SERIALIZED_IMDB + filename)
        lines.append(movie.get_csv_representation())

    writeCSV(FULL_CSV_PATH, lines, WIKI_MOVIE_PROPS)


def create_kb():
    path = "data/serialized_movies/"
    movies = [deserialize(path + movie) for movie in all_files_in_path(path)]

    with open("data/kb/knowledge_base.kfb", "w", encoding="utf-8") as file:
        for i, movie in enumerate(movies):
            print(f'Writing statements for film {i}/{len(movies)}')
            formatted_statements = movie.get_statements()
            file.write("\n".join(formatted_statements))
            file.write("\n")
