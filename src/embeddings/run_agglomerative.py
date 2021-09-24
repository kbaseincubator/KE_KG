import os
import pickle

os.getcwd()
os.chdir('/global/cfs/cdirs/kbase/ke_prototype/KE_KG')

from sklearn.cluster import AgglomerativeClustering
import numpy as np
from numpy import genfromtxt
from matplotlib import pyplot as plt

#skip column names
data = genfromtxt('./SkipGram_embedding_merged_imgvr_mg_good__cosine.tsv', delimiter='\t')#,names=True

data.shape
#remove row names from numpy array
data = data[:,1:]
data.shape


model = AgglomerativeClustering(distance_threshold=0, n_clusters=None)#, affinity="euclidean", linkage="ward")

clustering = model.fit(1.0 - data)


pickle.dump( model, open( "agglomerative_model.p", "wb" ) )
pickle.dump( clustering, open( "agglomerative_clustering.p", "wb" ) )
np.set_printoptions(threshold=np.inf)

with open('agglomerative.txt', 'w') as f:
    f.write(str(clustering))
with open('agglomerative_cluster_labels.txt', 'w') as f:
    f.write(clustering.labels_)

#np.savetxt('agglomerative.txt', clustering, delimiter='\t')
np.savetxt('agglomerative_cluster_labels.txt', clustering.labels_, delimiter='\t')



def plot_dendrogram(model, **kwargs):
    # Create linkage matrix and then plot the dendrogram

    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack([model.children_, model.distances_,
                                      counts]).astype(float)

    # Plot the corresponding dendrogram
    dendrogram(linkage_matrix, **kwargs)

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