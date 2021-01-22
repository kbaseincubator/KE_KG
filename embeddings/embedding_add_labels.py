import pandas as pd
import numpy as np

data = np.load("../IMGVR/SkipGram_embedding_IMGVR_sample.npy")
df = pd.DataFrame(data)

print(df.shape)

nodes = df.read_csv("./data/transform/imgvr/IMGVR_sample_KGX_nodes.tsv")


df.to_csv("../IMGVR/SkipGram_embedding_IMGVR_sample.tsv", sep="\t")