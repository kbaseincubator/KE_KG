import os
import pickle
os.getcwd()

os.chdir('/global/cfs/cdirs/kbase/ke_prototype/KE_KG')

from sklearn.cluster import DBSCAN
from sklearn.cluster import AgglomerativeClustering
import numpy as np
from numpy import genfromtxt
import pandas


#skip column names
data = genfromtxt('../embeddings/SkipGram_embedding_merged_imgvr_mg_good.csv', delimiter=',',skip_header=1)#,names=True

data.shape
#remove row names from numpy array
data = data[:,1:]
data.shape

clustering = DBSCAN(eps=3, min_samples=2).fit(data.astype(float))


pickle.dump( clustering, open( "dbscan_clustering.p", "wb" ) )


with open('dbscan.txt', 'w') as f:
    f.write(str(clustering))
with open('dbscan_cluster_labels.txt', 'w') as f:
    f.write(str(clustering.labels_))

#np.savetxt('dbscan.txt', clustering, delimiter='\t')
#np.savetxt('dbscan_cluster_labels.txt', clustering.labels_, delimiter='\t')

clustering.labels_
