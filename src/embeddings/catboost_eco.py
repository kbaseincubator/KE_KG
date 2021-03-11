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
null_value_stats = df_eco.isnull().sum(axis=0)
null_value_stats[null_value_stats != 0]


nzeros = [i for i,v in enumerate(df_eco.iloc[:,21:].sum()==0.0) if v==False]
columns = list(df_eco.iloc[:,0:21].columns)+list(df_eco.iloc[:,21:].iloc[:,nzeros].columns)
nzeros = [i for i,v in enumerate(df_eco.iloc[:,21:].sum(axis=1)==0.0) if v==False]
indices = list(df_eco.iloc[nzeros,21:].index)
df_ecoZ = df_eco[columns].loc[indices]
print(df_ecoZ.describe())
#df_ecoZ['Habitat_type'].value_counts()


y = df_ecoZ['IFR']
print(y)


X = df_ecoZ.iloc[:,(df_ecoZ.shape[1]-1):]
# Let's put the X's on a common scale
#scaler = MinMaxScaler()
#X[X.columns] = scaler.fit_transform(X)


X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=9) # The seed was 'chosen' so test and training contain all labels: rn=3,4,8,9
print("train label deficit:",len(set(y)-set(y_train)),"test label deficit:",len(set(y)-set(y_test)))

train_dataset = Pool(X_train, y_train)
test_dataset = Pool(X_test, y_test)

#class_counts = y_train.value_counts()
#max_count = max(class_counts)
#class_weights = {i:max_count/x for i,x in class_counts.iteritems()}
#print(class_weights)

iseed = 67

modelstart = time.time()
print(f"Starting training at {modelstart}")

cb_model = CatBoostRegressor(loss_function='RMSE',
                             iterations = 200,
                             verbose = 5,
                             learning_rate = 0.03,
                             depth = 2,
                             l2_leaf_reg = 0.5,
                             #eval_metric = 'MCC',
                             random_seed = iseed,
                             #bagging_temperature = 0.2,
                             #od_type = 'Iter',
                             #od_wait = 100
)


cbmf=cb_model.fit(X_train,y_train)
cbmf.feature_names = df_eco.columns[(df_ecoZ.shape[1]-1):]
#grid = {'iterations': [100],#[100, 150, 200],
##       'learning_rate': [0.03],#[0.03, 0.1],
#        'depth': [2],#[2, 4, 6, 8],
#        'l2_leaf_reg': [0.2]}#[0.2, 0.5, 1, 3]}
#cb_model.grid_search(grid, train_dataset)

print(f"Training finished in {time.time() - modelstart}s")

print(cbmf)
pickle.dump(cbmf,open("cbmf", "wb" ) )

pred = cb_model.predict(X_test)
rmse = (np.sqrt(mean_squared_error(y_test, pred)))
r2 = r2_score(y_test, pred)
print("Testing performance:")
print('RMSE: {:.2f}'.format(rmse))
print('R2: {:.2f}'.format(r2))


pickle.dump(pred,open("pred", "wb" ) )




#dill.dump_session('catboost_eco_model.db')




sorted_feature_importance = cb_model.feature_importances_.argsort()
plt.barh(cb_model.feature_names[sorted_feature_importance],
        cb_model.feature_importances_[sorted_feature_importance],
        color='turquoise')
plt.xlabel("CatBoost Feature Importance")
plt.savefig('feature_importance.pdf')



explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)
shap.summary_plot(shap_values, X_test, feature_names = cb_model.feature_names[sorted_feature_importance])

dill.dump_session('catboost_eco_all.db')
print('done')