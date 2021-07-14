#from fastdist import fastdist
import numpy as np
from numpy import genfromtxt

from timeit import default_timer as timer
from datetime import timedelta



start = timer()
embeddings = genfromtxt('../IMGVR/embeddings/SkipGram_embedding_merged_imgvr_mg_good.csv', delimiter=',')
end = timer()
print("read "+str(timedelta(seconds=end-start)))
print("shape "+str(embeddings.shape))
#cosine_sim = fastdist.matrix_pairwise_distance(embeddings, fastdist.cosine, "cosine", return_matrix=True)


# base similarity matrix (all dot products)
# replace this with A.dot(A.T).toarray() for sparse representation
start = timer()
similarity = np.dot(embeddings, embeddings.T)
end = timer()
print("dot "+str(timedelta(seconds=end-start)))
print("shape "+str(similarity.shape))

#  magnitude of preference vectors (number of occurrences)
start = timer()
square_mag = np.diag(similarity)
end = timer()
print("diag "+str(timedelta(seconds=end-start)))
print("shape "+str(square_mag.shape))

# inverse magnitude
start = timer()
inv_square_mag = 1 / square_mag
end = timer()
print("inverse "+str(timedelta(seconds=end-start)))
print("shape "+str(inv_square_mag.shape))

# replace inf with 0
start = timer()
inv_square_mag[np.isinf(inv_square_mag)] = 0
end = timer()
print("isinf "+str(timedelta(seconds=end-start)))

# square of the inverse magnitudestart = timer()
start = timer()
inv_mag = np.sqrt(inv_square_mag)
end = timer()
print("sqrt "+str(timedelta(seconds=end-start)))
print("shape "+str(inv_mag.shape))

# cosine similarity (elementwise multiply by inverse magnitudes)
start = timer()
cosine = similarity * inv_mag
end = timer()
print("sim * inv_mag"+str(timedelta(seconds=end-start)))
print("shape "+str(cosine.shape))

start = timer()
cosine = cosine.T * inv_mag
end = timer()
print("cosine.T * inv_mag"+str(timedelta(seconds=end-start)))
print("shape "+str(cosine.shape))

start = timer()
np.savetxt('../IMGVR/embeddings/SkipGram_embedding_merged_imgvr_mg_good__cosine.tsv.tsv', x, delimiter='\t')
end = timer()
print("write "+str(timedelta(seconds=end-start)))