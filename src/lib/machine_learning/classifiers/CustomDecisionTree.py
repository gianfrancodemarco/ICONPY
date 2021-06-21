from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier  # Import Decision Tree Classifier

from src.lib.machine_learning.CustomDataPreprocessor import CustomDataPreprocessor
from src.lib.machine_learning.CustomModel import MODEL_TYPES_ENUM, CustomModel


class CustomDecisionTree(CustomModel):

    def __init__(self, data_preprocessor: CustomDataPreprocessor = None):
        super().__init__(MODEL_TYPES_ENUM.CLASSIFIER, data_preprocessor)

    def train_and_evaluate(self):
        train_set, test_set = self._prepare_data()

        x_train = train_set.drop('metascore', axis=1)
        y_train = train_set['metascore']

        x_test = test_set.drop('metascore', axis=1)
        y_test = test_set['metascore']

        # self.__train_and_evaluate(x_train, x_test, y_train, y_test)
        # self.__train_and_evaluate(x_train, x_test, y_train, y_test, max_depth=20)
        # self.__train_and_evaluate(x_train, x_test, y_train, y_test, max_depth=30)
        # self.__train_and_evaluate(x_train, x_test, y_train, y_test, max_depth=50)  # best
        # self.__train_and_evaluate(x_train, x_test, y_train, y_test, criterion='entropy')
        # self.__train_and_evaluate(x_train, x_test, y_train, y_test, criterion='entropy', max_depth=20)
        # self.__train_and_evaluate(x_train, x_test, y_train, y_test, criterion='entropy', max_depth=30)
        # self.__train_and_evaluate(x_train, x_test, y_train, y_test, criterion='entropy', max_depth=50)
        #
        # self.__train_and_evaluate(x_train, x_test, y_train, y_test, max_depth=60)
        # self.__train_and_evaluate(x_train, x_test, y_train, y_test, max_depth=70)
        # self.__train_and_evaluate(x_train, x_test, y_train, y_test, max_depth=80)  # BEST 68.4
        # self.__train_and_evaluate(x_train, x_test, y_train, y_test, max_depth=90)
        # self.__train_and_evaluate(x_train, x_test, y_train, y_test, max_depth=100)
        #
        self.__train_and_evaluate(x_train, x_test, y_train, y_test, max_depth=50, min_impurity_decrease=.01)
        # self.__train_and_evaluate(x_train, x_test, y_train, y_test, max_depth=50, min_samples_split=10)


    def __train_and_evaluate(
            self,
            x_train,
            x_test,
            y_train,
            y_test,
            criterion='gini',
            max_depth=None,
            min_impurity_decrease=0.,
            min_samples_split=2
    ):
        # Create Decision Tree classifer object

        clf = DecisionTreeClassifier(
            criterion=criterion,
            max_depth=max_depth,
            min_impurity_decrease=min_impurity_decrease,
            min_samples_split=min_samples_split,
            random_state=42
        )

        # Train Decision Tree Classifer
        clf = clf.fit(x_train, y_train)

        # Predict the response for test dataset
        y_pred = clf.predict(x_test)

        # Model Accuracy, how often is the classifier correct?
        print(f'Criterion: {criterion}, max_depth: {max_depth}, min_samples_split: {min_samples_split}, min_impurity_decrease={min_impurity_decrease} ')
        print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
