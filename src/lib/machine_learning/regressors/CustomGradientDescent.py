import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

from src.lib.machine_learning.CustomModel import CustomModel


class CustomGradientDescent(CustomModel):

    def train_and_evaluate(self):
        train_set, test_set = self._prepare_data()

        x_train = train_set.drop('metascore', axis=1)
        y_train = train_set['metascore']

        x_test = test_set.drop('metascore', axis=1)
        y_test = test_set['metascore']

        x_train_np = np.array(x_train)
        y_train_np = np.array(y_train)

        x_test_np = np.array(x_test)
        y_test_np = np.array(y_test)

        regr = linear_model.SGDRegressor()

        regr.fit(x_train_np, y_train_np)

        y_pred = regr.predict(x_test_np)

        print("Mean squared error: %.2f" % mean_squared_error(y_test_np, y_pred))

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
