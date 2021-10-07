import sys
sys.setrecursionlimit(1000000)

import scipy.cluster.hierarchy as shc

from matplotlib import pyplot
from numpy import genfromtxt

#data = genfromtxt('../embeddings/SkipGram_embedding_merged_imgvr_mg_good.csv', delimiter=',', skip_header=1)

#data = genfromtxt('../../KE-Catboost/ziming/GO/data/go_aggregated_4.1/go_aggregated_4.1_mixed_updated_normalized_removed_zeros.tsv', delimiter='\t', skip_header=1)

data = genfromtxt('../../KE-Catboost/ziming/taxonomy/data/taxonomy_v4.1/taxonomy_aggregated_4.1_row_filtered_feature_selected_filtered_row_and_col.tsv', delimiter='\t', skip_header=1)


data.shape
#remove row labels
data = data[:,5:]#taxonomy
data = data.transpose()
#data = data[:,8:]#GO
data.shape

pyplot.figure(figsize=(10, 7))  
pyplot.title("Dendrogram")
dend = shc.dendrogram(shc.linkage(data, method='ward'))

pyplot.savefig('dendrogram_T.png')
