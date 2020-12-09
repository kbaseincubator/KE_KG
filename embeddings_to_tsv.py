import pandas as pd
import numpy as np

data = np.load("../IMGVR/20201205/SkipGram_embedding.npy")
df = pd.DataFrame(data)
df.to_csv("../IMGVR/20201205/SkipGram_embedding.tsv", sep="\t")