import pacmap
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import binascii
from sklearn.preprocessing import minmax_scale

# loading preprocessed coil_20 dataset
# you can change it with any dataset that is in the ndarray format, with the shape (N, D)
# where N is the number of samples and D is the dimension of each sample
##X = np.load("./data/coil_20.npy", allow_pickle=True)
##X = X.reshape(X.shape[0], -1)
##y = np.load("./data/coil_20_labels.npy", allow_pickle=True)

embedding_path = "/global/scratch/marcin/N2V/KE_KG/data/SkipGram_embedding_merged_imgvr_mg_good.csv"
nodes_path = "/global/scratch/marcin/N2V/KE_KG/data/merged_imgvr_mg_nodes_good.tsv"
X = pd.read_csv(embedding_path,sep=",", index_col=0, header=0)#
y = pd.read_csv(nodes_path,sep="\t", index_col=0, header=0)#

# initializing the pacmap instance
# Setting n_neighbors to "None" leads to a default choice shown below in "parameter" section
embedding = pacmap.PaCMAP(n_dims=2, n_neighbors=None, MN_ratio=0.5, FP_ratio=2.0)

# fit the data (The index of transformed data corresponds to the index of the original data)
X_transformed = embedding.fit_transform(X.to_numpy(), init="random")
np.save("KG_IMGVRMG_X_transformed_default.npy", X_transformed)

y_int = y['category'].values
for i in range(0, len(y_int)):
    y_int[i] = int(binascii.hexlify(y_int[i].encode("utf-8")), 16)

#y_int_norm = y_int/np.linalg.norm(y_int)
#y_int_norm = scale( y_int, axis=0, with_mean=True, with_std=True, copy=True )
#y_int_norm /= np.max(y_int)
y_int_norm = minmax_scale(y_int, feature_range=(0,1))
y_int_norm_unique = np.unique(y_int_norm)

count = 0
#assumes < 10 categories/colors
for y in y_int_norm_unique:
    print("y "+str(y))
    print("count "+str(count))
    print("len1 "+str(len(y_int_norm[y_int_norm == y])))
    y_int_norm[y_int_norm == y] = count * 10
    print("len2 "+str(len(y_int_norm[y_int_norm == count])))
    count+= 1

y_int_norm/=10

np.unique(y_int_norm)
# visualize the embedding
fig, ax = plt.subplots(1, 1, figsize=(6, 6))
ax.scatter(X_transformed[:, 0], X_transformed[:, 1], cmap="Accent", c=y_int_norm, s=0.6)

#ax.scatter(X_transformed[:, 0], X_transformed[:, 1], cmap="Spectral", s=0.6)

#save the visualization
plt.savefig("KG_IMGVRMG_pacmap.png")