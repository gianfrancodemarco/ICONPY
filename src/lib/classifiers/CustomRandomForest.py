from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier  # Import Decision Tree Classifier

from src.lib.classifiers.CustomDataPreprocessor import CustomDataPreprocessor


class CustomRandomForest:

    def __init__(self):
        dataPreprocessor = CustomDataPreprocessor()
        dataPreprocessor.do_preprocess()

        self.train_set = dataPreprocessor.train_set
        self.test_set = dataPreprocessor.test_set
        self.tree = None

    def __prepare_data(self):
        train_set = self.train_set
        test_set = self.test_set

        for _set in [train_set, test_set]:
            _set['duration'] = _set['duration'].cat.codes
            _set['metascore'] = _set['metascore'].cat.codes

        return [train_set, test_set]

    def train_and_evaluate(self):
        train_set, test_set = self.__prepare_data()

        x_train = train_set.drop('metascore', axis=1)
        y_train = train_set['metascore']

        x_test = test_set.drop('metascore', axis=1)
        y_test = test_set['metascore']

        self.__train_and_evaluate(x_train, x_test, y_train, y_test)
        self.__train_and_evaluate(x_train, x_test, y_train, y_test, n_estimators=100)
        self.__train_and_evaluate(x_train, x_test, y_train, y_test, n_estimators=200)
        self.__train_and_evaluate(x_train, x_test, y_train, y_test, n_estimators=200)
        self.__train_and_evaluate(x_train, x_test, y_train, y_test, n_estimators=300)
        self.__train_and_evaluate(x_train, x_test, y_train, y_test, n_estimators=400)
        self.__train_and_evaluate(x_train, x_test, y_train, y_test, n_estimators=500)
        self.__train_and_evaluate(x_train, x_test, y_train, y_test, n_estimators=500, min_samples_spit=10)


    def __train_and_evaluate(
            self,
            x_train,
            x_test,
            y_train,
            y_test,
            n_estimators=100,
            criterion='gini',
            max_depth=None,
            min_samples_spit=2
    ):
        # Create Decision Tree classifer object

        rfc = RandomForestClassifier(
            n_estimators=n_estimators,
            criterion=criterion,
            max_depth=max_depth,
            min_samples_spit=min_samples_spit,
            random_state=42
        )

        # Train Decision Tree Classifer
        rfc = rfc.fit(x_train, y_train)

        # Predict the response for test dataset
        y_pred = rfc.predict(x_test)

        # Model Accuracy, how often is the classifier correct?
        print(f'N_estimators: {n_estimators}, Criterion: {criterion}, max_depth: {max_depth}')
        print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
