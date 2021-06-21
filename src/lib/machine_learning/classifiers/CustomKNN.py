import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.neighbors import KNeighborsClassifier

from src.lib.machine_learning.CustomDataPreprocessor import CustomDataPreprocessor
from src.lib.machine_learning.CustomModel import CustomModel, MODEL_TYPES_ENUM


class CustomKNN(CustomModel):

    def __init__(self, data_preprocessor: CustomDataPreprocessor = None):
        super().__init__(MODEL_TYPES_ENUM.CLASSIFIER, data_preprocessor)

    def plot_k_estimates(self, min_k=1, max_k=25):

        train_set, test_set = self._prepare_data()

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

        print("Max accuracy: ", max(scores_list))

        plt.plot(k_range, scores_list)
        plt.xlabel('Value of K')
        plt.ylabel('Testing accuracy')
