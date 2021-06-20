from sklearn.neighbors import KNeighborsClassifier

from src.lib.classifiers.CustomDataPreprocessor import CustomDataPreprocessor
from sklearn import metrics

import matplotlib.pyplot as plt


class CustomKNN:

    def __init__(self):
        dataPreprocessor = CustomDataPreprocessor()
        dataPreprocessor.do_preprocess()

        self.train_set = dataPreprocessor.train_set
        self.test_set = dataPreprocessor.test_set

    def __prepare_data(self):
        train_set = self.train_set
        test_set = self.test_set

        for set in [train_set, test_set]:
            set['duration'] = set['duration'].cat.codes
            set['metascore'] = set['metascore'].cat.codes

        return [train_set, test_set]

    def plot_k_estimates(self, min_k=1, max_k=25):

        train_set, test_set = self.__prepare_data()

        k_range = range(min_k, max_k + 1)
        scores = {}
        scores_list = []

        x_train = train_set.drop('metascore', axis=1)
        y_train = train_set['metascore']

        x_test = test_set.drop('metascore', axis=1)
        y_test = test_set['metascore']

        for k in k_range:
            knn = KNeighborsClassifier(n_neighbors=k)
            knn.fit(x_train, y_train)
            y_pred = knn.predict(x_test)
            scores[k] = metrics.accuracy_score(y_test, y_pred)
            scores_list.append(scores[k])

        plt.plot(k_range, scores_list)
        plt.xlabel('Value of K')
        plt.ylabel('Testing accuracy')