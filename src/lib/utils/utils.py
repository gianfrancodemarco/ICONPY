from os import listdir
from os.path import isfile, join
from .csvutils import readCSVtoObj


def clean_string(filename, replacer='', extend_invalid=None):

    invalid = '<>:"/\|?* '

    if extend_invalid is not None:
        invalid += extend_invalid

    for char in invalid:
        filename = filename.replace(char, replacer)

    return filename


def all_files_in_path(path):
    return [f for f in listdir(path) if isfile(join(path, f))]


def get_skipped_movies_ids():
    path = 'data/serialized_movies_full'

    fetched_movies_ids = [filename.split('_')[0] for filename in all_files_in_path(path)]
    all_movies_ids = [movie["uri"].split("/")[-1] for movie in
                      readCSVtoObj("data/_old_dataset_with_uris.csv", ["_", "_", "uri"])]

    skipped_ids = [idx for idx in all_movies_ids if idx not in fetched_movies_ids]
    return skipped_ids
