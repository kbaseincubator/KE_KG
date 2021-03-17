import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.inspection import permutation_importance

import sys
import os
import time
from catboost import CatBoostClassifier, CatBoostRegressor, Pool, cv
import pickle
import seaborn as sns

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import shap


random_seed = 123

print("start")

df_eco = pd.read_csv('../Torben_metaG_GTDB-taxa-count_summary_GOLDfivetuple_merged_v1.tsv', sep='\t', index_col=0, encoding='utf-8')
print(df_eco.head())


df_eco.shape
df_eco_orig = df_eco

#remove singleton environments
y_counts = df_eco.loc[:,'GOLD_five_tuple'].value_counts()
#require minimum category members = 3
keep_envs = y_counts[y_counts > 2].index

#df_eco_ = df_eco_orig
df_eco = df_eco[df_eco['GOLD_five_tuple'].isin(keep_envs)]
df_eco.shape

y_counts2 = df_eco.loc[:,'GOLD_five_tuple'].value_counts()
print(y_counts2)

y = df_eco['GOLD_five_tuple']
print(y)

X = df_eco.loc[:, df_eco.columns != 'GOLD_five_tuple']#df_eco.iloc[:,:-1]
print(X.columns)
print("X "+str(X.shape))


# Let's put the X's on a common scale
scaler = MinMaxScaler()
X[X.columns] = scaler.fit_transform(X)
# Let's make the categories ordinal
habitat_ord={h:i for i,h in enumerate(set(y))}
inv_map = {v: k for k, v in habitat_ord.items()}
#X

len(y.unique())

#describe = X.describe()

##groups = y#np.array([1, 1, 2, 2, 2, 3, 3, 3])
##gss = GroupShuffleSplit(n_splits=1, train_size=.75, random_state=random_seed)
##gss.get_n_splits()

#train_inds, test_inds = next(GroupShuffleSplit(test_size=.20, n_splits=1, random_state = random_seed).split(X, groups=y))
#X_train = X.iloc[train_inds]
#X_test = X.iloc[test_inds]
#y_train = y.iloc[train_inds]#pd.Series(y.to_numpy()[train_inds])
#y_test = y.iloc[test_inds]#pd.Series(y.to_numpy()[test_inds])


#for train_idx, test_idx in gss.split(X, y, groups):
#    print("TRAIN:", train_idx, "TEST:", test_idx)
#X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=random_seed) #, random_state=9# The seed was 'chosen' so test and training contain all labels: rn=3,4,8,9
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=random_seed)
X_train.shape
X_test.shape
len(y_train)
len(y_test)
print("train label deficit:",len(set(y)-set(y_train)),"test label deficit:",len(set(y)-set(y_test)))


#X_test = X_test[y_test[y_test.isin(y_train)]]
#y_test = y_test[y_test.isin(y_train)]

###check if env in test missing in training and if so remove?
#y_test[~y_test.isin(y_train)]


print("shapes "+str(X_train.shape)+"\t"+str(X_test.shape)+"\t"+str(y_train.shape)+"\t"+str(y_test.shape))

train_dataset = Pool(X_train, y_train)
test_dataset = Pool(X_test, y_test)

input_data_dump = [random_seed, X, y, X_train, X_test, y_train, y_test]
pickle.dump(input_data_dump,open("input_data_dump_v3", "wb" ) )



class_counts = y_train.value_counts()
max_count = max(class_counts)
class_weights = {i:max_count/x for i,x in class_counts.iteritems()}
class_weights


# Optimize hyperparameters with grid_search
iseed = 123

cb_model_grid = CatBoostClassifier(
    iterations=50,
    verbose=5,
    learning_rate=0.02,
    depth=5,
    l2_leaf_reg=1,
    eval_metric='MCC',
    random_seed=iseed,
    bagging_temperature=0.2,
    od_type='Iter',
    od_wait=100,
    class_weights=class_weights)

#grid = {'learning_rate': [0.01, 0.1, 0.2],
#        'depth': [4, 5, 6],
#        'l2_leaf_reg': [0.5, 1, 5]}
#lr 0.2 de 6 l2 1
grid = {'learning_rate': [0.3, 0.4, 0.5],
        'depth': [5, 6,7],
       'l2_leaf_reg': [0.5, 1, 5]}

modelstart = time.time()
print(f"Starting model parameter optimization at {modelstart}")

grid_search_result = cb_model_grid.grid_search(grid, X=X_train, y=y_train,verbose=5)
lr = grid_search_result['params']['learning_rate']
de = grid_search_result['params']['depth']
l2 = grid_search_result['params']['l2_leaf_reg']

print(f"Finished in {time.time() - modelstart}s")

print("lr "+str(lr)+" de "+str(de)+" l2 "+str(l2))
#lr 0.5 de 7 l2 1

#iseed = 123

cb_model = CatBoostClassifier(
    iterations=200,
    verbose=5,
    learning_rate=lr,
    depth=de,
    l2_leaf_reg=l2,
    eval_metric='MCC',
    random_seed = iseed,
    bagging_temperature = 0.2,
    od_type='Iter',
    od_wait=100,
    class_weights=class_weights,
)


modelstart = time.time()
print(f"Starting training at {modelstart}")
cbmpf = cb_model.fit(X_train, y_train)
print(f"Training finished in {time.time() - modelstart}s")


cbmpf.feature_names = df_eco.columns[1:]

predictions = cbmpf.predict(X_test)
predictions_probs = cbmpf.predict_proba(X_test)


explainer_model = shap.TreeExplainer(cb_model)
explainer_fit = shap.TreeExplainer(cbmpf)

confusion_matrix = get_confusion_matrix(cb_model, Pool(X_train, y_train))
confusion_matrix_test = get_confusion_matrix(cb_model, Pool(X_test, y_test))

data_output = [random_seed, grid, grid_search_result, cb_model, cbmpf, predictions, explainer_model, predictions_probs, explainer_fit, confusion_matrix]#,confusion_matrix_test]
pickle.dump(data_output,open("data_output_v3", "wb" ) )
data_output = [random_seed, grid, grid_search_result, cb_model, cbmpf, predictions, explainer_model, predictions_probs, explainer_fit, confusion_matrix,confusion_matrix_test]
pickle.dump(data_output,open("data_output_v3_all", "wb" ) )

sys.exit()




sorted_feature_importance = cb_model.feature_importances_.argsort()
plt.figure(figsize=(20,10))
plt.barh(cb_model.feature_names[sorted_feature_importance][-50:],
        cb_model.feature_importances_[sorted_feature_importance][-50:],
        color='turquoise')
plt.xlabel("CatBoost Feature Importance")


