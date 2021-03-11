# Requirements and imports

import subprocess
import sys
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.inspection import permutation_importance

import time
from catboost import CatBoostClassifier, CatBoostRegressor, Pool, cv
import dill
import pickle
import seaborn as sns

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import shap



random_seed = 123


print("start")

df_eco = pd.read_csv('/global/homes/m/marcinj/graphs/eco/Datasets/Marginal_Combined_60.csv', sep=',', encoding='utf-8')
print(df_eco.head())

#bin_width = (max(df_eco['IFR']) - min(df_eco['IFR']))/3
#bins = [0, bin_width, 2*bin_width]
#names = ['low', 'medium', 'high', '35-65', '65+']
#bin_dict = dict(enumerate(names, 1))
#IFR_orig = df['IFR']
#df['IFR'] = np.vectorize(bin_dict.get)(np.digitize(df_eco['IFR'], bins))

# How many vals are null?
#null_value_stats = df_eco.isnull().sum(axis=0)
#null_value_stats[null_value_stats != 0]


print(df_eco.describe())


y = df_eco['IFR']
print(y)

print("df_eco "+str(df_eco.shape))

X = df_eco.iloc[:,:-1]

print("X "+str(X.shape))
# Let's put the X's on a common scale
#scaler = MinMaxScaler()
#X[X.columns] = scaler.fit_transform(X)


X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=random_seed) #, random_state=9# The seed was 'chosen' so test and training contain all labels: rn=3,4,8,9
print("train label deficit:",len(set(y)-set(y_train)),"test label deficit:",len(set(y)-set(y_test)))

print("shapes "+str(X_train.shape)+"\t"+str(X_test.shape)+"\t"+str(y_train.shape)+"\t"+str(y_test.shape))

train_dataset = Pool(X_train, y_train)
test_dataset = Pool(X_test, y_test)

input_data_dump = [X, y, X_train, X_test, y_train, y_test]
pickle.dump(input_data_dump,open("input_data_dump", "wb" ) )

#class_counts = y_train.value_counts()
#max_count = max(class_counts)
#class_weights = {i:max_count/x for i,x in class_counts.iteritems()}
#print(class_weights)


modelstart = time.time()
print(f"Starting grid search at {modelstart}")

cb_model = CatBoostRegressor(loss_function='RMSE',
                             iterations = 200,
                             verbose = 5,
                             learning_rate = 0.03,
                             depth = 2,
                             l2_leaf_reg = 0.5,
                             #eval_metric = 'MCC',
                             random_seed = random_seed,
                             #bagging_temperature = 0.2,
                             #od_type = 'Iter',
                             #od_wait = 100
)


grid = {#'iterations': [100, 150, 200],
       'learning_rate': [0.1, 0.2],
        'depth': [5, 6, 7],
        'l2_leaf_reg': [3, 6, 9]}
grid_search_result = cb_model.grid_search(grid, train_dataset)

lr = grid_search_result['params']['learning_rate']
de = grid_search_result['params']['depth']
l2 = grid_search_result['params']['l2_leaf_reg']

print(f"Trainedgrid search in {time.time() - modelstart}s")

print("lr, de, l2 "+str(lr)+", "+str(de)+", "+str(l2))


print(f"Starting at {modelstart}")

cb_model = CatBoostRegressor(loss_function='RMSE',
                             iterations = 200,
                             verbose = 5,
                             learning_rate = lr,
                             depth = de,
                             l2_leaf_reg = l2,
                             #eval_metric = 'MCC',
                             random_seed = random_seed,
                             #bagging_temperature = 0.2,
                             #od_type = 'Iter',
                             #od_wait = 100
)

cbmf = cb_model.fit(X_train,y_train)


pred_train = cb_model.predict(X_train)
rmseT = (np.sqrt(mean_squared_error(y_train, pred_train)))
r2T = r2_score(y_train, pred_train)
print("Testing performance:")
print('RMSE training: {:.2f}'.format(rmseT))
print('R2 training: {:.2f}'.format(r2T))


print("range "+str((df_eco.shape[1]-1)))
cbmf.feature_names = df_eco.columns[:-1]
print("names "+str(len(cbmf.feature_names)))

print(f"Trained in {time.time() - modelstart}s")


pred_test = cb_model.predict(X_test)
rmse = (np.sqrt(mean_squared_error(y_test, pred_test)))
r2 = r2_score(y_test, pred_test)
print("Testing performance:")
print('RMSE: {:.2f}'.format(rmse))
print('R2: {:.2f}'.format(r2))

explainer_model = shap.TreeExplainer(cb_model)
explainer_fit = shap.TreeExplainer(cbmf)

data_output = [random_seed, grid, grid_search_result, cb_model, cbmf, pred_train, explainer_model, pred_test, explainer_fit]
pickle.dump(data_output,open("data_output", "wb" ) )


print('done')
