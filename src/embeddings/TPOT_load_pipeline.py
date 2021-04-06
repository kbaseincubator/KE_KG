import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.metrics import f1_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
import eli5

from deap import creator
from sklearn.model_selection import cross_val_score
from tpot.export_utils import generate_pipeline_code
from tpot.export_utils import expr_to_tree

#tpot.export('tpot_Marginal_Combined_60.pipeline.py')
pipeline_str = "RandomForestRegressor(SelectFwe(StandardScaler(input_matrix), alpha=0.016), bootstrap=False, max_features=0.5, min_samples_leaf=3, min_samples_split=2, n_estimators=100) TPOTRegressor(generations=10, population_size=50, random_state=123, scoring='r2', verbosity=2)"

tpot_pipeline = creator.Individual.from_string(pipeline_str, tpot._pset)
sklearn_pipeline = tpot._toolbox.compile(expr=tpot_pipeline)

sklearn_pipeline_str = generate_pipeline_code(expr_to_tree(tpot_pipeline, tpot._pset), tpot.operators)
print(sklearn_pipeline_str)

# Fix random state when the operator allows  (optional) just for get consistent CV score
#tpot._set_param_recursive(sklearn_pipeline.steps, 'random_state', 123)

try:
    cv_scores = cross_val_score(sklearn_pipeline, training_features, training_target, cv=5, scoring='accuracy', verbose=0)
    mean_cv_scores = np.mean(cv_scores)
except Exception as e:
    print(e)
    mean_cv_scores = -float('inf')
print(mean_cv_scores)
