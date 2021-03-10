# Requirements and imports

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import time
from catboost import CatBoostClassifier
from catboost import CatBoostClassifier, Pool, cv
import dill
import seaborn as sns

import matplotlib
import matplotlib.pyplot as plt
import numpy as np


df_eco = pd.read_csv('/global/homes/m/marcinj/graphs/eco/Datasets/Marginal_Combined_60.csv', sep=',', encoding='utf-8')
df_eco.head()

bin_width = (max(df_eco['IFR']) - min(df_eco['IFR']))/3
bins = [0, bin_width, 2*bin_width]
names = ['low', 'medium', 'high', '35-65', '65+']
bin_dict = dict(enumerate(names, 1))
IFR_orig = df['IFR']
df['IFR'] = np.vectorize(bin_dict.get)(np.digitize(df_eco['IFR'], bins))

#df['IFR'] = np.vectorize(d.get)(np.digitize(df['IFR'], bins))

df_eco['IFR'] = pd.qcut(df_eco['IFR'], q=4)

# How many vals are null?
null_value_stats = df_eco.isnull().sum(axis=0)
null_value_stats[null_value_stats != 0]


nzeros = [i for i,v in enumerate(df_eco.iloc[:,21:].sum()==0.0) if v==False]
columns = list(df_eco.iloc[:,0:21].columns)+list(df_eco.iloc[:,21:].iloc[:,nzeros].columns)
nzeros = [i for i,v in enumerate(df_eco.iloc[:,21:].sum(axis=1)==0.0) if v==False]
indices = list(df_eco.iloc[nzeros,21:].index)
df_ecoZ = df_eco[columns].loc[indices]
df_ecoZ.describe()
#df_ecoZ['Habitat_type'].value_counts()


y = df_ecoZ['IFR']
y


X = df_ecoZ.iloc[:,21:]
# Let's put the X's on a common scale
scaler = MinMaxScaler()
X[X.columns] = scaler.fit_transform(X)


X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=9) # The seed was 'chosen' so test and training contain all labels: rn=3,4,8,9
print("train label deficit:",len(set(y)-set(y_train)),"test label deficit:",len(set(y)-set(y_test)))

class_counts = y_train.value_counts()
max_count = max(class_counts)
class_weights = {i:max_count/x for i,x in class_counts.iteritems()}
class_weights

# Optimize hyperparameters with grid_search
iseed = 67

cb_model = CatBoostClassifier(
    iterations=50,
    verbose=5,
    learning_rate=0.02,
    depth=5,
    eval_metric='MCC',
    random_seed=iseed,
    bagging_temperature=0.2,
    od_type='Iter',
    od_wait=100)#,
#    class_weights=class_weights)

grid = {'learning_rate': [0.06, 0.1,0.14],
        'depth': [5, 6, 7],
        'l2_leaf_reg': [0.5, 1, 5]}
#grid = {'learning_rate': [0.06, 0.1,0.14],
#        'depth': [5, 6, 7],
#        'l2_leaf_reg': [0.5, 1, 5]}

modelstart = time.time()
print(f"Starting model parameter optimization at {modelstart}")

#grid_search_result = cb_model.grid_search(grid, X=X_train, y=y_train,verbose=5)
#lr = grid_search_result['params']['learning_rate']
#de = grid_search_result['params']['depth']
#l2 = grid_search_result['params']['l2_leaf_reg']

lr = 0.02
de = 5
l2 = 1


print(f"Finished in {time.time() - modelstart}s")

iseed = 52

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
    od_wait=100)#,
    #class_weights=class_weights,
#)


modelstart = time.time()
print(f"Starting training at {modelstart}")
cbmpf = cb_model.fit(X_train, y_train);
print(f"Training finished in {time.time() - modelstart}s")

cbmpf

predictions = cbmpf.predict(X_test)
predictions_probs = cbmpf.predict_proba(X_test)


print(predictions[:20])
print(y_test[:20])
print(predictions_probs[:10])
# list(zip(predictions[:10], predictions_probs[:10]))

fea_imp = pd.DataFrame({'imp': cb_model.feature_importances_, 'col': X.columns})
fea_imp = fea_imp.sort_values(['imp', 'col'], ascending=[True, False]).iloc[-50:]
plot1 = fea_imp.plot(kind='barh', x='col', y='imp', figsize=(20, 10))
plot1.savefig('feature_importance.pdf')


y_predict = list(flatten(cbmf.predict(X_test)))
confusion_matrix_test = confusion_matrix(y_test, y_predict)
# Confusion matrix comes out in natural sort order of classes

poset = sorted(list(set(y_test) | set(y_predict)))
ilabels = ['Actual ' + x for x in poset]
plabels = ['Predicted ' + x for x in poset]

confusion_matrix_test = pd.DataFrame(confusion_matrix_test,
                                     index=ilabels,
                                     columns=plabels)

ytcounts = {x: list(y_test).count(x) for x in sorted(list(set(poset)))}

for i in confusion_matrix_test.index:
    d = ytcounts[i.split(' ')[1]]
    d = 1.0 if d == 0 else d
    confusion_matrix_test.loc[i] = confusion_matrix_test.loc[i].div(d)

# display(confusion_matrix_train)
plt.figure(figsize=(13, 7))
plot2 = sns.heatmap(confusion_matrix_test, annot=True, linewidths=0.1, annot_kws={"fontsize": 8})
plot2.savefig('confusion_matrix.pdf')

dill.dump_session('catboost_eco.db')
print('done')