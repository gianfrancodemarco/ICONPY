from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier  # Import Decision Tree Classifier

from src.lib.classifiers.CustomDataPreprocessor import CustomDataPreprocessor


class CustomDecisionTree:

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
        self.__train_and_evaluate(x_train, x_test, y_train, y_test, max_depth=20)
        self.__train_and_evaluate(x_train, x_test, y_train, y_test, max_depth=30)
        self.__train_and_evaluate(x_train, x_test, y_train, y_test, max_depth=50)
        self.__train_and_evaluate(x_train, x_test, y_train, y_test, criterion='entropy')
        self.__train_and_evaluate(x_train, x_test, y_train, y_test, criterion='entropy', max_depth=20)
        self.__train_and_evaluate(x_train, x_test, y_train, y_test, criterion='entropy', max_depth=30)
        self.__train_and_evaluate(x_train, x_test, y_train, y_test, criterion='entropy', max_depth=50)

    def __train_and_evaluate(self, x_train, x_test, y_train, y_test, criterion='gini', max_depth=None):
        # Create Decision Tree classifer object

        clf = DecisionTreeClassifier(criterion=criterion, max_depth=max_depth)

        # Train Decision Tree Classifer
        clf = clf.fit(x_train, y_train)

        # Predict the response for test dataset
        y_pred = clf.predict(x_test)

        # Model Accuracy, how often is the classifier correct?
        print(f'Criterion: {criterion}, max_depth: {max_depth}')
        print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
