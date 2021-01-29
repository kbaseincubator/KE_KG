import pandas as pd
import numpy as np

data = np.load("../IMGVR/SkipGram_embedding_IMGVR_merged_final_embedding.npy")
df = pd.DataFrame(data)

print(df.shape)

nodes = pd.read_csv("./data/merged/merged_kg/IMGVR_merged_final_kg_nodes.tsv", sep="\t")

df.set_index(nodes['id'])

df.to_csv("../IMGVR/SkipGram_embedding_IMGVR_merged_final_embedding_wids.tsv", sep="\t")