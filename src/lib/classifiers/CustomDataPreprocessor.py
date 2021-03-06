import os
import sys

import pandas as pd

from sklearn.model_selection import train_test_split

from src.lib.utils.serializeutils import deserialize
from src.lib.utils.utils import all_files_in_path

module_path = os.path.abspath(os.path.join('../..'))
sys.path.append(module_path)

DATA_PATH = '../../resources/data/serialized_movies_with_imdb_score/'
DATASET_ATTRIBUTES = [
    "main_subject", "genre", "country_of_origin", "director", "screenwriter", "cast_member",
    "director_of_photography", "film_editor", "composer", "producer", "production_company",
    "distributed_by", "narrative_location", "filming_location", "duration", "metascore"
]
ATTRIBUTES_TO_BINARIZE = [
    "main_subject", "genre", "country_of_origin", "director", "screenwriter", "cast_member",
    "director_of_photography", "film_editor", "composer", "producer", "production_company",
    "distributed_by", "narrative_location", "filming_location"]


class CustomDataPreprocessor:

    def __init__(self):
        self.dataset = None
        self.test_set = None
        self.train_set = None

    def do_preprocess(self):
        self.__load_data()
        self.__remove_missing_metascore()
        self.__remove_attributes()
        self.__extract_plain_data()
        self.__binarize_dataset()
        self.__drop_sparse_column()
        self.__discretize_columns()
        self.__split_dataset()

    def __load_data(self):

        self.dataset = []

        for movie in all_files_in_path(DATA_PATH):
            self.dataset.append(deserialize(DATA_PATH + movie))

    def __remove_missing_metascore(self):
        new_data = []
        for movie in self.dataset:
            if 'metascore' in movie.props and movie.props['metascore'] != 'N/A':
                new_data.append(movie)
        self.dataset = new_data

    def __remove_attributes(self):
        for movie in self.dataset:
            new_props = {}
            for attr in DATASET_ATTRIBUTES:
                if attr in movie.props:
                    new_props[attr] = movie.props[attr]
                else:
                    new_props[attr] = '0'
            movie.props = new_props

    def __extract_plain_data(self):

        dataset = []

        for movie in self.dataset:
            plain_movie_data = {}
            for prop in movie.props:
                value = movie.props[prop]

                if type(value) != dict and type(value) != list:
                    plain_value = value
                elif type(value) == dict:
                    plain_value = value['value']
                else:
                    plain_value = ",".join([el['value'] for el in value])

                if prop == 'duration':  # there are multiple values
                    plain_value = int(float(min(plain_value.split(','))))

                plain_movie_data[prop] = plain_value

            dataset.append(plain_movie_data)

        self.dataset = dataset

    def __binarize_dataset(self):
        df = pd.DataFrame(self.dataset)

        for attr in ATTRIBUTES_TO_BINARIZE:
            dummies = df[attr].str.get_dummies(sep=',').add_prefix(f'{attr}_')
            df = pd.concat([df, dummies], axis=1).drop(attr, 1)
        df = df.loc[:, ~df.columns.duplicated()]

        self.dataset = df

    def __drop_sparse_column(self, threshold=2):
        to_drop = []

        for col in self.dataset.columns:
            if (self.dataset[col] != 0).sum() < threshold:
                to_drop.append(col)

        self.dataset.drop(to_drop, axis=1, inplace=True)

    def __discretize_columns(self):
        # self.dataset['metascore'] = pd.cut(pd.to_numeric(self.dataset['metascore']), bins=[0, 54.5, 100]) --> 1621 mediocre 1617 good
        self.dataset['metascore'] = pd.cut(pd.to_numeric(self.dataset['metascore']),
                                           bins=[0, 60, 100], labels=["Mediocre", "Good"])  # --> 1981 mediocre 1257 good

        self.dataset['duration'] = pd.cut(pd.to_numeric(self.dataset['duration']), bins=3, labels=["Short", "Medium", "Long"])

    def __split_dataset(self):
        self.train_set, self.test_set = train_test_split(
            self.dataset,
            train_size=0.7,
            test_size=0.3,
            random_state=42
        )

        # re-orders the indexes
        self.train_set = self.train_set.reset_index(drop=True)
        self.test_set = self.test_set.reset_index(drop=True)
