import pandas as pd
import numpy as np

data = np.load("../IMGVR/SkipGram_embedding_IMGVR_merged_final_embedding.npy")
df = pd.DataFrame(data)

print(df.shape)

df.to_csv("../IMGVR/SkipGram_embedding_IMGVR_merged_final_embedding.tsv", sep="\t")