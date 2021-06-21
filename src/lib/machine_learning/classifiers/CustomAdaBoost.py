# Load libraries
from sklearn.ensemble import AdaBoostClassifier
from sklearn import datasets

# Import train_test_split function
from sklearn.model_selection import train_test_split

#Import scikit-learn metrics module for accuracy calculation
from sklearn import metrics
from sklearn.svm import SVC

from src.lib.machine_learning.CustomDataPreprocessor import CustomDataPreprocessor
from src.lib.machine_learning.CustomModel import MODEL_TYPES_ENUM, CustomModel


class CustomAdaBoost(CustomModel):

    def __init__(self, data_preprocessor: CustomDataPreprocessor = None):
        super().__init__(MODEL_TYPES_ENUM.CLASSIFIER, data_preprocessor)

    def train_and_evaluate(self):
        train_set, test_set = self._prepare_data()

        x_train = train_set.drop('metascore', axis=1)
        y_train = train_set['metascore']

        x_test = test_set.drop('metascore', axis=1)
        y_test = test_set['metascore']

        # self.__train_and_evaluate(x_train, x_test, y_train, y_test, n_estimators=50)
        # self.__train_and_evaluate(x_train, x_test, y_train, y_test, n_estimators=100)
        # self.__train_and_evaluate(x_train, x_test, y_train, y_test, n_estimators=150)
        # self.__train_and_evaluate(x_train, x_test, y_train, y_test, n_estimators=200)
        #
        # self.__train_and_evaluate(x_train, x_test, y_train, y_test, learning_rate=0.9)
        # self.__train_and_evaluate(x_train, x_test, y_train, y_test, learning_rate=0.8)
        # self.__train_and_evaluate(x_train, x_test, y_train, y_test, learning_rate=0.7)
        # self.__train_and_evaluate(x_train, x_test, y_train, y_test, learning_rate=0.6)
        # self.__train_and_evaluate(x_train, x_test, y_train, y_test, learning_rate=0.5)

        # self.__train_and_evaluate(x_train, x_test, y_train, y_test, n_estimators=100, learning_rate=1.1)
        # self.__train_and_evaluate(x_train, x_test, y_train, y_test, n_estimators=100, learning_rate=1.2)
        # self.__train_and_evaluate(x_train, x_test, y_train, y_test, n_estimators=100, learning_rate=0.9)
        # self.__train_and_evaluate(x_train, x_test, y_train, y_test, n_estimators=100, learning_rate=0.8)
        # self.__train_and_evaluate(x_train, x_test, y_train, y_test, n_estimators=100, learning_rate=0.7)
        # self.__train_and_evaluate(x_train, x_test, y_train, y_test, n_estimators=100, learning_rate=0.6)  # BEST 0.70
        # self.__train_and_evaluate(x_train, x_test, y_train, y_test, n_estimators=100, learning_rate=0.5)


    def __train_and_evaluate(
            self,
            x_train,
            x_test,
            y_train,
            y_test,
            base_estimator=None,
            n_estimators=50,
            learning_rate=1
    ):
        # Create adaboost classifer object
        abc = AdaBoostClassifier(
            base_estimator=base_estimator,
            n_estimators=n_estimators,
            learning_rate=learning_rate
        )

        # Train Adaboost Classifer
        model = abc.fit(x_train, y_train)

        # Predict the response for test dataset
        y_pred = model.predict(x_test)

        # Model Accuracy, how often is the classifier correct?
        print(f'n_estimators: {n_estimators}, learning_rate: {learning_rate}')
        print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
