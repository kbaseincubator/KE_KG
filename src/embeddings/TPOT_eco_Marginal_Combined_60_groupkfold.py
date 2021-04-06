from tpot import TPOTRegressor#TPOTClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectFwe
from sklearn.ensemble import RandomForestRegressor
#from sklearn.metrics import SCORERS
from tpot.metrics import SCORERS
from sklearn.pipeline import make_pipeline
from sklearn.metrics import r2_score
import numpy as np
import pandas as pd

random_seed = 123

print("start")

df_eco = pd.read_csv('/global/homes/m/marcinj/graphs/eco/Datasets/Marginal_Combined_60.csv', sep=',', index_col=0, encoding='utf-8')
print(df_eco.head())


dataframe_list_list = np.empty((10, 5)).tolist()
for i in range(0, 10):
    for j in range(0, 5):
        dataframe_list_list[i][j] = pd.read_csv('./CV_Sets/Marginal_Combined_60/Set_'+str(i+1)+'/Fold_'+str(j+1)+'.csv', sep=',', index_col=0, encoding='utf-8')
        #print(df_cur.head())

train_X_list_list = np.empty((10, 5)).tolist()
test_X_list_list = np.empty((10, 5)).tolist()
train_y_list_list = np.empty((10, 5)).tolist()
test_y_list_list = np.empty((10, 5)).tolist()

for i in range(0, 10):
    for j in range(0, 5):
        print(str(i) + "\t" + str(j))

        df_cur = dataframe_list_list[i][j]
        # df_cur = df_cur.drop(['FIPS'], axis=1)
        # df_cur = df_cur.drop(['Set_Type'], axis=1)
        y = df_cur['IFR']
        # print(y)

        print("df_cur " + str(df_cur.shape))

        # X = df_cur#.iloc[:,:-1]
        # X.drop(['FIPS'], axis=1, inplace=True)
        # print(X.columns)
        # print("X "+str(X.shape))
        X_train = df_cur[dataframe_list_list[i][j]['Set_Type'] == 'Training']
        X_test = df_cur[dataframe_list_list[i][j]['Set_Type'] == 'Test']
        y_train = df_cur[dataframe_list_list[i][j]['Set_Type'] == 'Training']['IFR']
        y_test = df_cur[dataframe_list_list[i][j]['Set_Type'] == 'Test']['IFR']
        print("shapes " + str(X_train.shape) + "\t" + str(X_test.shape) + "\t" + str(y_train.shape) + "\t" + str(
            y_test.shape))

        # print(y_train)
        X_train.drop(['Set_Type'], axis=1, inplace=True)
        X_train.drop(['FIPS'], axis=1, inplace=True)
        X_train.drop(['IFR'], axis=1, inplace=True)
        X_test.drop(['Set_Type'], axis=1, inplace=True)
        X_test.drop(['FIPS'], axis=1, inplace=True)
        X_test.drop(['IFR'], axis=1, inplace=True)

        print("train label deficit:", len(set(y) - set(y_train)), "test label deficit:", len(set(y) - set(y_test)))

        print("shapes " + str(X_train.shape) + "\t" + str(X_test.shape) + "\t" + str(y_train.shape) + "\t" + str(
            y_test.shape))

        # train_dataset = Pool(X_train, y_train)
        # test_dataset = Pool(X_test, y_test)
        train_X_list_list[i][j] = X_train
        test_X_list_list[i][j] = X_test
        train_y_list_list[i][j] = y_train
        test_y_list_list[i][j] = y_test



y_counts = df_eco.loc[:,'FIPS'].value_counts()
#require minimum category members = 3
keep_envs = y_counts[y_counts > 2].index

#df_eco_ = df_eco_orig
df_eco = df_eco[df_eco['FIPS'].isin(keep_envs)]
df_eco.shape

y_counts2 = df_eco.loc[:,'FIPS'].value_counts()
print(y_counts2)


stratify_data = df_eco['FIPS']

df_eco = df_eco.drop(['FIPS'], axis=1)
y = df_eco['IFR']
print(y)

print("df_eco "+str(df_eco.shape))

X = df_eco.iloc[:,:-1]
print(X.columns)
print("X "+str(X.shape))



tpot = TPOTRegressor(generations=20, population_size=100, verbosity=5, random_state=random_seed, scoring="r2")
tpot.fit(train_X_list_list[0][2],train_y_list_list[0][2])
print(tpot.score(test_X_list_list[0][2], test_y_list_list[0][2]))
tpot.export('tpot_Marginal_Combined_60_CV_0_2.pipeline.py')
print(tpot.export())

#tpot = TPOTRegressor(generations=10, population_size=50, verbosity=2, random_state=random_seed, scoring="r2")
#[0][0]
#Best pipeline: ExtraTreesRegressor(ExtraTreesRegressor(LinearSVR(ExtraTreesRegressor(input_matrix, bootstrap=False, max_features=0.25, min_samples_leaf=6, min_samples_split=16, n_estimators=100), C=0.001, dual=True, epsilon=0.1, loss=squared_epsilon_insensitive, tol=0.0001), bootstrap=False, max_features=0.6500000000000001, min_samples_leaf=10, min_samples_split=10, n_estimators=100), bootstrap=False, max_features=0.45, min_samples_leaf=5, min_samples_split=16, n_estimators=100)
#TPOTRegressor(generations=10, population_size=50, random_state=123,
#              scoring='r2', verbosity=2)
#0.9832844487368682
#0.28894625465876445

results_train = tpot.predict(train_X_list_list[0][2])
results = tpot.predict(test_X_list_list[0][2])


r2Tr = r2_score(train_y_list_list[0][2], results_train)
print(r2Tr)
r2T = r2_score(test_y_list_list[0][2], results)
print(r2T)

tpot.fitted_pipeline_


extracted_best_model = tpot.fitted_pipeline_.steps[-1][1]
extracted_best_model.fit(X, y)
exctracted_best_model.feature_importances_
