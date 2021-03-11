# Requirements and imports


import pickle
import seaborn as sns

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import shap

from catboost import CatBoostClassifier, CatBoostRegressor, Pool, cv




print("start")

df_eco = pd.read_csv('/global/homes/m/marcinj/graphs/eco/Datasets/Marginal_Combined_60.csv', sep=',', encoding='utf-8')
print(df_eco.head())



input_data = pickle.load(open( "./catboost_out/input_data_dump", "rb" ))
#[X, y, X_train, X_test, y_train, y_test]

X = input_data[0]
y = input_data[1]
X_train = input_data[2]
X_test = input_data[3]
y_train = input_data[4]
y_test = input_data[5]

train_dataset = Pool(X_train, y_train)
test_dataset = Pool(X_test, y_test)


output_data = pickle.load(open( "./catboost_out/data_output", "rb" ))
#[random_seed, grid, grid_search_result, cb_model, cbmf, pred_train, explainer_model, pred_test, explainer_fit]

random_seed = output_data[0]
grid = output_data[1]
grid_search_result = output_data[2]
cb_model = output_data[3]
cbmf = output_data[4]
pred_train = output_data[5]
explainer_model = output_data[6]
pred_test = output_data[7]
explainer_fit = output_data[8]


sorted_feature_importance = cb_model.feature_importances_.argsort()
plt.barh(cb_model.feature_names[sorted_feature_importance[1:100]],
        cb_model.feature_importances_[sorted_feature_importance[1:100]],
        color='turquoise')
plt.xlabel("CatBoost Feature Importance")
plt.savefig('feature_importance.pdf')



shap_values = explainer.shap_values(X_test)
shap.summary_plot(shap_values, X_test, feature_names = cb_model.feature_names[sorted_feature_importance],show=False)#,matplotlib=True).savefig('SHAP.pdf',bbox_inches = 'tight')

f = plt.gcf()
f.savefig('SHAP.pdf')

shap.force_plot(explainer.expected_value, shap_values, X_test, feature_names = cb_model.feature_names[sorted_feature_importance],show=False)#.savefig('SHAP.pdf',bbox_inches = 'tight')
f = plt.gcf()
f.savefig('force_plot.pdf')


print('done')
