from src.lib.machine_learning.classifiers.CustomAdaBoost import CustomAdaBoost
from src.lib.machine_learning.CustomDataPreprocessor import CustomDataPreprocessor
from src.lib.machine_learning.classifiers.CustomDecisionTree import CustomDecisionTree
from src.lib.machine_learning.classifiers.CustomRandomForest import CustomRandomForest

data_preprocessor = CustomDataPreprocessor()
data_preprocessor.do_preprocess(discretize=False)

print("------ KNN ------")
#knn_model = CustomKNN(data_preprocessor)
#knn_model.plot_k_estimates()


print("\n\n------ DT ------")
#tree_model = CustomDecisionTree(data_preprocessor)
#tree_model.train_and_evaluate()

print("\n\n------ RF ------")
#random_forest_model = CustomRandomForest(data_preprocessor)
#random_forest_model.train_and_evaluate()

print("\n\n------ ADABOOST -------")
#random_forest_model = CustomAdaBoost(data_preprocessor)
#random_forest_model.train_and_evaluate()
