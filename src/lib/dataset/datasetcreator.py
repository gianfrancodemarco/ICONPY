import logging
import os
import shutil
import zipfile
from pathlib import Path
from time import sleep

from src import ROOT_DIR
from src.lib.omdbapi.omdbapi import get_movie
from src.lib.utils.serializeutils import deserialize, serialize
from src.lib.utils.utils import all_files_in_path, readCSVtoListOfDict, writeCSV, create_zip_file
from src.lib.wikidata.WikiMovie import WikiMovie, WIKI_MOVIE_PROPS
from src.lib.wikidata.WikidataAPI import do_query
from src.lib.wikidata.queryFactor import create_query, MOVIE_QUERY, ENTITY_QUERY

DATASET = os.path.join(ROOT_DIR, "src/resources/data/1_dataset.csv")
DATASET_WITH_URIS = os.path.join(ROOT_DIR, "src/resources/data/2_dataset_with_uris.csv")
SERIALIZED_ZIP = os.path.join(ROOT_DIR, "src/resources/data/3_movies.zip")
SERIALIZED_WITH_METASCORE_ZIP = os.path.join(ROOT_DIR, "src/resources/data/4_movies_imdb.zip")
DATASET_FULL = os.path.join(ROOT_DIR, "src/resources/data/1.1_dataset_full.csv")
KNOWLEDGE_BASE = os.path.join(ROOT_DIR, "src/resources/data/knowledge_base.kfb")

TMP_FOLDER = os.path.join(ROOT_DIR, "src/resources/tmp")
TMP_FOLDER2 = os.path.join(ROOT_DIR, "src/resources/tmp2")

logger = logging.getLogger('logger')


def __get_uris(source_file=DATASET, dest_file=DATASET_WITH_URIS):
    """

    :param source_file: The original dataset: a csv with the cols: id, title
    :param dest_file: The csv that will contain the updated dataset in the form of: id, title, uri
    :return: Makes a query to WikiData for every movie in source_file and gets the uri of the resource.
    Writes the updated dataset in dest_file

    """

    # load all movies
    data = readCSVtoListOfDict(source_file)

    try:
        # already fetched movies
        already_fetched = readCSVtoListOfDict(dest_file)
        logger.info(f'Total movies: {len(data)}')

        # start from the last fecthed
        i = int(already_fetched[-1]['id'])
        to_fetch = data[i:]

    except FileNotFoundError:
        open(dest_file, "w")  # creates the file

        # writes the headers
        writeCSV(
            dest_file,
            [['id', 'title', 'uri']],
            mode='a'
        )

        i = 0
        to_fetch = data

    # fetches the movies
    for movie in to_fetch:

        logger.debug(f'Getting movie {i + 1} / {len(data)}')

        query = create_query(MOVIE_QUERY, [movie['title']])
        results = do_query(query)

        if results is None or len(results) == 0:
            i += 1
            continue

        result_movie = results[0]  # take the first result (better matching)
        row = [movie['id'], movie['title'], result_movie['movie']['value']]

        writeCSV(
            dest_file,
            [row],
            mode='a'
        )

        i += 1


def get_uris():
    """

    Wrapper for __get_uris.
    If an exception is thrown, waites for 10 minutes and tries again

    """
    try:
        __get_uris()
    except Exception as e:
        print(e)
        sleep(600)
        get_uris()


def __get_entities(zip_file=SERIALIZED_ZIP, source_file=DATASET_WITH_URIS):
    # load all movies
    data = readCSVtoListOfDict(source_file)
    logger.debug(f'{len(data)} movies to fetch')

    # create TMP_FOLDER if doesn't exist
    Path(TMP_FOLDER).mkdir(parents=True, exist_ok=True)

    # if the zip with the serialized films exists, unzip in temp folder
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(TMP_FOLDER)
    except FileNotFoundError:
        logger.debug("No serialized movie found")
    except zipfile.BadZipFile:
        logger.error("Bad zip file. Deleting.")
        os.remove(zip_file)

    # find the last serialized movie
    serialized_movies_filenames = all_files_in_path(TMP_FOLDER)

    all_wiki_data_ids = [movie['uri'].split('/')[-1] for movie in data]
    serialized_wiki_data_ids = 0
    # if any has been serialized, update the movies to serialize
    if len(serialized_movies_filenames) > 0:
        serialized_wiki_data_ids = [filename.split('_')[0] for filename in serialized_movies_filenames]
        wiki_data_id_to_fetch = [wiki_data_id for wiki_data_id in all_wiki_data_ids if
                                 wiki_data_id not in serialized_wiki_data_ids]
    else:
        wiki_data_id_to_fetch = all_wiki_data_ids

    for i, wiki_data_id in enumerate(wiki_data_id_to_fetch):

        print(f'Getting entity {i + len(serialized_wiki_data_ids) + 1} / {len(data)}')

        query = create_query(ENTITY_QUERY, [wiki_data_id])
        results = do_query(query)

        wiki_movie = WikiMovie(results)
        wiki_movie.build_full()
        wiki_movie.set_prop("wiki_data_id", wiki_data_id)

        try:
            wiki_movie.serialize(TMP_FOLDER)
        except KeyError as e:
            print(f'Error on movie: {i + len(serialized_wiki_data_ids)}')
            print(e)
            continue

    # get all serialized movies
    serialized_movies_filenames = all_files_in_path(TMP_FOLDER)

    create_zip_file(SERIALIZED_ZIP, TMP_FOLDER, serialized_movies_filenames)

    # delete tmp folder
    try:
        shutil.rmtree(TMP_FOLDER)
    except OSError as e:
        logger.error("Error: %s : %s" % (TMP_FOLDER, e.strerror))


def get_entities():
    try:
        __get_entities()
    except Exception as e:
        logger.critical(e)
        sleep(600)
        get_entities()


def get_metascores():
    try:
        __get_metascores()
    except Exception as e:
        logger.critical(e)
        sleep(600)
        get_metascores()


def __get_metascores(source_zip_file=SERIALIZED_ZIP, dest_zip_file=SERIALIZED_WITH_METASCORE_ZIP):
    # create TMP_FOLDER if doesn't exist
    Path(TMP_FOLDER).mkdir(parents=True, exist_ok=True)

    # extract the source_zip_file to get all movies
    try:
        with zipfile.ZipFile(source_zip_file, 'r') as zip_ref:
            zip_ref.extractall(TMP_FOLDER)
    except Exception:
        logger.critical("Could not extract source zip")
        return

    # create TMP_FOLDER2 if doesn't exist
    Path(TMP_FOLDER2).mkdir(parents=True, exist_ok=True)

    # extract the source_zip_file to get movies that already have metascore
    try:
        with zipfile.ZipFile(dest_zip_file, 'r') as zip_ref:
            zip_ref.extractall(TMP_FOLDER2)
    except FileNotFoundError:
        logger.debug("No serialized movies with metascore found")
    except zipfile.BadZipFile:
        logger.error("Bad zip file. Deleting.")
        os.remove(dest_zip_file)

    all_movies = all_files_in_path(TMP_FOLDER)
    already_fetched_movies = all_files_in_path(TMP_FOLDER2)

    to_fetch = [movie for movie in all_movies if movie not in already_fetched_movies]

    for i, file in enumerate(to_fetch):
        print(f"Deserializing: {i + 1}/{len(to_fetch)}")
        movie = deserialize(f'{TMP_FOLDER}/{file}')

        if "IMDb_ID" in movie.props:

            if type(movie.props['IMDb_ID']) == list:
                id = movie.props['IMDb_ID'][0]['value']
            else:
                id = movie.props['IMDb_ID']['value']

            result = get_movie(id).json()

            movie.set_prop("metascore", result["Metascore"])
            movie.set_prop("imdbrating", result["imdbRating"])
            movie.set_prop("imdbvotes", result["imdbVotes"])

        movie.build()
        serialize(movie, f'{TMP_FOLDER2}/{file}')

    # delete tmp folder
    try:
        shutil.rmtree(TMP_FOLDER)
    except OSError as e:
        logger.error("Error: %s : %s" % (TMP_FOLDER, e.strerror))

    # get all serialized movies
    serialized_movies_filenames = all_files_in_path(TMP_FOLDER2)

    create_zip_file(SERIALIZED_WITH_METASCORE_ZIP, TMP_FOLDER2, serialized_movies_filenames)

    # delete tmp folder2
    try:
        shutil.rmtree(TMP_FOLDER2)
    except OSError as e:
        logger.error("Error: %s : %s" % (TMP_FOLDER2, e.strerror))


def write_full_csv():
    # create TMP_FOLDER if doesn't exist
    Path(TMP_FOLDER).mkdir(parents=True, exist_ok=True)

    # extract the source_zip_file to get all movies
    try:
        with zipfile.ZipFile(SERIALIZED_WITH_METASCORE_ZIP, 'r') as zip_ref:
            zip_ref.extractall(TMP_FOLDER)
    except Exception:
        logger.critical("Could not extract source zip")
        return

    lines = []
    to_insert = all_files_in_path(TMP_FOLDER)

    for filename in to_insert:
        movie = deserialize(f'{TMP_FOLDER}/{filename}')
        lines.append(movie.get_csv_representation())

    writeCSV(DATASET_FULL, lines, WIKI_MOVIE_PROPS)

    # delete tmp folder
    try:
        shutil.rmtree(TMP_FOLDER)
    except OSError as e:
        logger.error("Error: %s : %s" % (TMP_FOLDER, e.strerror))


def write_kb():
    # create TMP_FOLDER if doesn't exist
    Path(TMP_FOLDER).mkdir(parents=True, exist_ok=True)

    # extract the source_zip_file to get all movies
    try:
        with zipfile.ZipFile(SERIALIZED_WITH_METASCORE_ZIP, 'r') as zip_ref:
            zip_ref.extractall(TMP_FOLDER)
    except Exception:
        logger.critical("Could not extract source zip")
        return

    movies = [deserialize(f'{TMP_FOLDER}/{movie}') for movie in all_files_in_path(TMP_FOLDER)]

    with open(KNOWLEDGE_BASE, "w", encoding="utf-8") as file:
        for i, movie in enumerate(movies):
            logger.debug(f'Writing statements for film {i}/{len(movies)}')
            formatted_statements = movie.get_statements()
            file.write("\n".join(formatted_statements))
            file.write("\n")

    # delete tmp folder
    try:
        shutil.rmtree(TMP_FOLDER)
    except OSError as e:
        logger.error("Error: %s : %s" % (TMP_FOLDER, e.strerror))


def dataset_pipeline():
    get_uris()
    get_entities()
    get_metascores()
    # write_full_csv()
    write_kb()
