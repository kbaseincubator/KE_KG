from tpot import TPOTRegressor#TPOTClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectFwe
from sklearn.ensemble import RandomForestRegressor
#from sklearn.metrics import SCORERS
from tpot.metrics import SCORERS
from sklearn.pipeline import make_pipeline
import numpy as np
import pandas as pd

random_seed = 123

print("start")

df_eco = pd.read_csv('/global/homes/m/marcinj/graphs/eco/Datasets/Marginal_Combined_60.csv', sep=',', index_col=0, encoding='utf-8')
print(df_eco.head())

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


X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.75, test_size=0.25, stratify=stratify_data, random_state=random_seed)
print("train label deficit:",len(set(y)-set(y_train)),"test label deficit:",len(set(y)-set(y_test)))

print("shapes "+str(X_train.shape)+"\t"+str(X_test.shape)+"\t"+str(y_train.shape)+"\t"+str(y_test.shape))

#tpot = TPOTClassifier(generations=, population_size=50, verbosity=2, random_state=random_seed)
tpot = TPOTRegressor(generations=10, population_size=50, verbosity=2, random_state=random_seed, scoring="r2")
tpot.fit(X_train, y_train)
print(tpot.score(X_test, y_test))
tpot.export('tpot_Marginal_Combined_60.pipeline.py')
print(tpot.export())

results = tpot.predict(X_test)

#Best pipeline: RandomForestRegressor(SelectFwe(StandardScaler(input_matrix), alpha=0.016), bootstrap=False, max_features=0.5, min_samples_leaf=3, min_samples_split=2, n_estimators=100)
#TPOTRegressor(generations=10, population_size=50, random_state=123,
#              scoring='r2', verbosity=2)
#>>> print(tpot.score(X_test, y_test))
#0.998496134596775

#exported_pipeline = make_pipeline(
#    RandomForestRegressor(
#        LassoLarsCV(input_matrix, normalize=False), bootstrap=False, max_features=0.55, min_samples_leaf=3, min_samples_split=17, n_estimators=100)
#)

#RandomForestRegressor(LassoLarsCV(input_matrix, normalize=False), bootstrap=False, max_features=0.55, min_samples_leaf=3, min_samples_split=17, n_estimators=100)
#0.9941451434709654

print(tpot.export())
print(tpot.named_steps['selectfwe'].get_support())


print(dict(list(tpot.evaluated_individuals_.items())[0:2]))

export_pipeline = tpot.export()

tpot_pipeline = creator.Individual.from_string(pipeline_str, tpot._pset)
sklearn_pipeline = tpot._toolbox.compile(expr=tpot_pipeline)

sklearn_pipeline_str = generate_pipeline_code(expr_to_tree(tpot_pipeline, tpot._pset), tpot.operators)
print(sklearn_pipeline_str)

for pipeline_string in sorted(tpot.evaluated_individuals_.keys()):
    print(pipeline_string)
    deap_pipeline = creator.Individual.from_string(pipeline_string, tpot._pset)
    sklearn_pipeline = tpot._toolbox.compile(expr=deap_pipeline)
    # print sklearn pipeline string
    sklearn_pipeline_str = generate_pipeline_code(expr_to_tree(deap_pipeline, tpot._pset), tpot.operators)
    print(sklearn_pipeline_str)


best_pipeline_str =  make_pipeline(
    StandardScaler(),
    SelectFwe(score_func="f_regression", alpha=0.016),
    RandomForestRegressor(bootstrap=False, max_features=0.5, min_samples_leaf=3, min_samples_split=2, n_estimators=100)
)


deap_pipeline = creator.Individual.from_string(best_pipeline_str, tpot._pset)
sklearn_pipeline = tpot._toolbox.compile(expr=deap_pipeline)
# print sklearn pipeline string
sklearn_pipeline_str = generate_pipeline_code(expr_to_tree(deap_pipeline, tpot._pset), tpot.operators)
print(sklearn_pipeline_str)


###BROKEN, for classifiers??
best_pipeline = tpot.fitted_pipeline_
holdout_r2 = SCORERS['r2'](
                          best_pipeline,
                          X_test,
                          y_test
                      )
# neg_mean_squared_error
holdout_recall = SCORERS['recall'](
                          best_pipeline,
                          X_test,
                          y_test
                      )
holdout_precision = SCORERS['precision'](
                          best_pipeline,
                          X_test,
                          y_test
                      )
holdout_f1 = SCORERS['f1'](
                          best_pipeline,
                          X_test,
                          y_test
                      )
holdout_roc_auc = SCORERS['roc_auc'](
                          best_pipeline,
                          X_test,
                          y_test
                      )

print("R2 "+holdout_r2)
print("recall "+holdout_r2)
print("precision "+holdout_r2)
print("f1 "+holdout_r2)
print("roc_auc "+holdout_r2)