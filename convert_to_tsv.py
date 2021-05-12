import pandas as pd
import numpy as np

data = np.load("../IMGVR/SkipGram_embedding.npy")
df = pd.DataFrame(data)
df.to_csv("../IMGVR/SkipGram_embedding.tsv", sep="\t")