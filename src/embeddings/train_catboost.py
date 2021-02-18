from catboost import CatBoostClassifier

import pandas as pd


pos_df = pd.read_csv('../IMGVR/link_predict_IMGVR_sample_extra_v3/virus_host__subtract.tsv', sep=",", header=0, index_col=0)
neg_df = pd.read_csv('../IMGVR/link_predict_IMGVR_sample_extra_v3/virus_host_NEGATIVE__subtract.tsv', sep=",", header=0, index_col=0)

dimpos = pos_df.shape
dimneg = neg_df.shape
print(dimpos)
print(dimneg)

train_data = pd.concat([pos_df, neg_df], axis=0)

print(dimpos[0])
print([1] * dimpos[0])


train_labels = [1] * dimpos[0]  + [0] * dimneg[0]

#train_data = [[0, 3],
#              [4, 1],
#              [8, 1],
#              [9, 1]]
#train_labels = [0, 0, 1, 1]

model = CatBoostClassifier(iterations=10 #,
                           #task_type="GPU",
                           #devices='0:1'
                           )
out = model.fit(train_data,
          train_labels,
          verbose=True)

print(out)