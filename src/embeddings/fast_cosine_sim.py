#from fastdist import fastdist
import numpy as np
from numpy import genfromtxt

from timeit import default_timer as timer
from datetime import timedelta



start = timer()
#embeddings = genfromtxt('../embeddings/SkipGram_embedding_merged_imgvr_mg_good_100.csv', delimiter=',', names=True, dtype=e)

labels = np.genfromtxt('../embeddings/SkipGram_embedding_merged_imgvr_mg_good.csv', delimiter=',', usecols=0, dtype=str)
embeddings = np.genfromtxt('../embeddings/SkipGram_embedding_merged_imgvr_mg_good.csv', delimiter=',')[:,1:]
#embeddings = {label: row for label, row in zip(labels, raw_data)}

end = timer()
print("read "+str(timedelta(seconds=end-start)))
print("shape "+str(embeddings.shape))
#cosine_sim = fastdist.matrix_pairwise_distance(embeddings, fastdist.cosine, "cosine", return_matrix=True)
np.savetxt('SkipGram_embedding_merged_imgvr_mg_good__embeddings_0.tsv', embeddings, delimiter='\t')


# base similarity matrix (all dot products)
# replace this with A.dot(A.T).toarray() for sparse representation
start = timer()
similarity = np.dot(embeddings, embeddings.T)
end = timer()
print("dot "+str(timedelta(seconds=end-start)))
print("shape "+str(similarity.shape))

#np.savetxt('SkipGram_embedding_merged_imgvr_mg_good__similarity_1.tsv', similarity, delimiter='\t')

#  magnitude of preference vectors (number of occurrences)
start = timer()
square_mag = np.diag(similarity)
end = timer()
print("diag "+str(timedelta(seconds=end-start)))
print("shape "+str(square_mag.shape))
#np.savetxt('SkipGram_embedding_merged_imgvr_mg_good__sq_mag_2.tsv', square_mag, delimiter='\t')

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
#np.savetxt('SkipGram_embedding_merged_imgvr_mg_good__inv_sq_mag_3.tsv', inv_square_mag, delimiter='\t')

# square of the inverse magnitudestart
start = timer()
inv_mag = np.sqrt(inv_square_mag)
end = timer()
print("sqrt "+str(timedelta(seconds=end-start)))
print("shape "+str(inv_mag.shape))
#np.savetxt('SkipGram_embedding_merged_imgvr_mg_good__inv_mag_4.tsv', inv_mag, delimiter='\t')

# cosine similarity (elementwise multiply by inverse magnitudes)
start = timer()
cosine = similarity * inv_mag
end = timer()
print("sim * inv_mag "+str(timedelta(seconds=end-start)))
print("shape "+str(cosine.shape))

#np.savetxt('SkipGram_embedding_merged_imgvr_mg_good__sim__inv_mag_5.tsv', cosine, delimiter='\t')

start = timer()
cosine = cosine.T * inv_mag
end = timer()
print("cosine.T * inv_mag "+str(timedelta(seconds=end-start)))
print("shape "+str(cosine.shape))

start = timer()
np.savetxt('SkipGram_embedding_merged_imgvr_mg_good__cosine.tsv', cosine, fmt='%1.3f', delimiter='\t')
#labels_ar = np.asarray(labels)
labels.tofile('SkipGram_embedding_merged_imgvr_mg_good__cosine_labels.tsv',sep='\t',format='%s')
#np.savetxt('SkipGram_embedding_merged_imgvr_mg_good__cosine_labels.tsv', labels_ar, delimiter='\t')
end = timer()
print("write "+str(timedelta(seconds=end-start)))
