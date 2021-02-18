from catboost import CatBoostClassifier

import pandas as pd
import numpy as np

from catboost import Pool, CatBoostRegressor
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer

from catboost import CatBoostClassifier, Pool, cv
from sklearn.metrics import accuracy_score
from sklearn import metrics
from sklearn.metrics import mean_squared_error
from sklearn import feature_selection
from sklearn.preprocessing import minmax_scale
from sklearn.preprocessing import MinMaxScaler

######  Plotting and Graphics

import matplotlib
import matplotlib.pyplot as plt

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
import seaborn as sns

###### Notebook storage library
import pickle
import dill


if len(sys.argv) < 2:
   sys.exit()
positive_training = sys.argv[1]
negative_training = sys.argv[2]

#'../IMGVR/link_predict_IMGVR_sample_extra_v3/virus_host__subtract.tsv'
#'../IMGVR/link_predict_IMGVR_sample_extra_v3/virus_host_NEGATIVE__subtract.tsv'
pos_df = pd.read_csv(positive_training, sep=",", header=0, index_col=0)
neg_df = pd.read_csv(negative_training, sep=",", header=0, index_col=0)

dimpos = pos_df.shape
dimneg = neg_df.shape
print(dimpos)
print(dimneg)

train_data = pd.concat([pos_df, neg_df], axis=0)

print(dimpos[0])
print([1] * dimpos[0])


train_labels = [1] * dimpos[0]  + [0] * dimneg[0]

#calc_feature_statistics(train_data,
#                        target=None,
#                        feature=None,
#                        prediction_type=None,
#                        cat_feature_values=None,
#                        plot=True,
#                        max_cat_features_on_plot=10,
#                        thread_count=-1,
#                        plot_file="calc_feature_statistics.pdf")


#train_data = [[0, 3],
#              [4, 1],
#              [8, 1],
#              [9, 1]]
#train_labels = [0, 0, 1, 1]

model = CatBoostClassifier(iterations=1000,
                           #task_type="GPU",
                           #devices='0:1'
                            verbose=True
                           )
out = model.fit(train_data,
          train_labels,
          verbose=True)

#cv_data = cv(Pool(X,y,cat_features=categorical_features_indices),model.get_params(),fold_count=10,verbose=False)

print(out)

feature_importance = model.get_feature_importance(type= "PredictionValuesChange")
print(feature_importance)

ax = sns.barplot(x=list(range(df.shape[0])), y=np.sort(feature_importance))
fig = ax.get_figure()
fig.savefig('feature_importance.png')