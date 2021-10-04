# Dendogram for Heirarchical Clustering
import scipy.cluster.hierarchy as shc

from matplotlib import pyplot
from numpy import genfromtxt

data = genfromtxt('../embeddings/SkipGram_embedding_merged_imgvr_mg_good.csv', delimiter=',')

pyplot.figure(figsize=(10, 7))  
pyplot.title("Dendrogram")
dend = shc.dendrogram(shc.linkage(data, method='ward'))

pyplot.savefig('dendrogram.png')
