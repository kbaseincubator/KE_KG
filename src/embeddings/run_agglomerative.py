import os

os.getcwd()

os.chdir('/global/cfs/cdirs/kbase/ke_prototype/KE_KG')

from sklearn.cluster import AgglomerativeClustering
import numpy as np
from numpy import genfromtxt
from matplotlib import pyplot as plt

#skip column names
data = genfromtxt('../embeddings/SkipGram_embedding_merged_imgvr_mg_good.csv', delimiter=',',skip_header=1)#,names=True

data.shape
#remove row names from numpy array
data = data[:,1:]
data.shape


model = AgglomerativeClustering(distance_threshold=0, n_clusters=None)
clustering = model.fit(data)

np.savetxt('agglomerative.txt', clustering, delimiter='\t')
np.savetxt('agglomerative_cluster_labels.txt', clustering.labels_, delimiter='\t')

clustering.labels_



plt.title('Hierarchical Clustering Dendrogram - top 5 levels')
# plot the top three levels of the dendrogram
plot_dendrogram(model, truncate_mode='level', p=5)
plt.xlabel("Number of points in node (or index of point if no parenthesis).")
plt.savefig('agglomerative_top5.png')

plt.title('Hierarchical Clustering Dendrogram')
# plot the top three levels of the dendrogram
plot_dendrogram(model)#, truncate_mode='level', p=3)
plt.xlabel("Number of points in node (or index of point if no parenthesis).")
plt.savefig('agglomerative_all.png')