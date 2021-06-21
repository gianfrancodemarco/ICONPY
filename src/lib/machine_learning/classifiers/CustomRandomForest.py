from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier  # Import Decision Tree Classifier

from src.lib.machine_learning.CustomDataPreprocessor import CustomDataPreprocessor
from src.lib.machine_learning.CustomModel import CustomModel, MODEL_TYPES_ENUM


class CustomRandomForest(CustomModel):

    def __init__(self, data_preprocessor: CustomDataPreprocessor = None):
        super().__init__(MODEL_TYPES_ENUM.CLASSIFIER, data_preprocessor)

    def train_and_evaluate(self):
        train_set, test_set = self._prepare_data()

        x_train = train_set.drop('metascore', axis=1)
        y_train = train_set['metascore']

        x_test = test_set.drop('metascore', axis=1)
        y_test = test_set['metascore']

        # self.__train_and_evaluate(x_train, x_test, y_train, y_test, n_estimators=100)
        # self.__train_and_evaluate(x_train, x_test, y_train, y_test, n_estimators=200)
        # self.__train_and_evaluate(x_train, x_test, y_train, y_test, n_estimators=300)
        # self.__train_and_evaluate(x_train, x_test, y_train, y_test, n_estimators=400)
        # self.__train_and_evaluate(x_train, x_test, y_train, y_test, n_estimators=500)
        # self.__train_and_evaluate(x_train, x_test, y_train, y_test, n_estimators=500, min_samples_spit=10)
        #
        # self.__train_and_evaluate(x_train, x_test, y_train, y_test, n_estimators=600) # BEST 0.6954732510288066
        # self.__train_and_evaluate(x_train, x_test, y_train, y_test, n_estimators=600, min_samples_spit=10)
        # self.__train_and_evaluate(x_train, x_test, y_train, y_test, n_estimators=500, min_samples_spit=5)
        # self.__train_and_evaluate(x_train, x_test, y_train, y_test, n_estimators=500, min_samples_spit=20)
        self.__train_and_evaluate(x_train, x_test, y_train, y_test, n_estimators=500, min_impurity_decrease=.01)

    def __train_and_evaluate(
            self,
            x_train,
            x_test,
            y_train,
            y_test,
            n_estimators=100,
            criterion='gini',
            max_depth=None,
            min_samples_spit=2,
            min_impurity_decrease=0.
    ):
        # Create Decision Tree classifer object

        rfc = RandomForestClassifier(
            n_estimators=n_estimators,
            criterion=criterion,
            max_depth=max_depth,
            min_samples_split=min_samples_spit,
            min_impurity_decrease=min_impurity_decrease,
            random_state=42
        )

        # Train Decision Tree Classifer
        rfc = rfc.fit(x_train, y_train)

        # Predict the response for test dataset
        y_pred = rfc.predict(x_test)

        # Model Accuracy, how often is the classifier correct?
        print(f'N_estimators: {n_estimators}, Criterion: {criterion}, max_depth: {max_depth}, min_samples_split: {min_samples_spit}, min_impurity_decrease: {min_impurity_decrease}')
        print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
