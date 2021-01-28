import pandas as pd
import numpy as np

data = np.load("../IMGVR/embeddings/SkipGram_IMGVR_merged_finalv2_kg_embedding.npy")
df = pd.DataFrame(data)

print(df.shape)

df.to_csv("../IMGVR/embeddings/SkipGram_IMGVR_merged_finalv2_kg_embedding.tsv", sep="\t")