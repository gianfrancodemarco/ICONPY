from statistics import mean

import numpy as np
from numpy import absolute, std
from sklearn import datasets, linear_model
from sklearn.linear_model import ElasticNet
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import RepeatedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler

from src.lib.machine_learning.CustomModel import CustomModel


class CustomElasticNet(CustomModel):

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

        # define model
        model = ElasticNet(alpha=1.0, l1_ratio=0.5, max_iter=20)
        # define model evaluation method

        model.fit(x_train_np, y_train_np)
        y_pred = model.predict(x_test_np)

        # cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
        # evaluate model
        # scores = cross_val_score(model, y_test, y_test_np, scoring='r_2', cv=cv, n_jobs=-1)
        # force scores to be positive
        # scores = absolute(scores)
        # print('Mean MAE: %.3f (%.3f)' % (mean(scores), std(scores)))
        print("Mean squared error: %.2f" % r2_score(y_test_np, y_pred))


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
