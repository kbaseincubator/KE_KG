import pandas as pd
import numpy as np

data = np.load("../IMGVR/embeddings/SkipGram_embedding_IMGVR_sample.npy")
df = pd.DataFrame(data)

nodes =

print(df.shape)

df.to_csv("../IMGVR/SkipGram_embedding_IMGVR_sample.tsv", sep="\t")