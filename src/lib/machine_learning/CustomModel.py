from enum import Enum

from src.lib.machine_learning.CustomDataPreprocessor import CustomDataPreprocessor


class MODEL_TYPES_ENUM(Enum):
    REGRESSOR = "REGRESSOR"
    CLASSIFIER = "CLASSIFIER"


class CustomModel:

    def __init__(self, model_type: MODEL_TYPES_ENUM, data_preprocessor=None):
        """

        :param model_type: "classifier or regressor"
        :param data_preprocessor:
        """

        if data_preprocessor is None:
            data_preprocessor = CustomDataPreprocessor()
            data_preprocessor.do_preprocess()

        self.train_set = data_preprocessor.train_set[:]
        self.test_set = data_preprocessor.test_set[:]
        self.model_type = model_type

    def _prepare_data(self):
        train_set = self.train_set
        test_set = self.test_set

        if self.model_type == MODEL_TYPES_ENUM.CLASSIFIER:
            for dataset in [train_set, test_set]:
                dataset['duration'] = dataset['duration'].cat.codes
                dataset['metascore'] = dataset['metascore'].cat.codes

        return [train_set, test_set]
