import pandas as pd
import numpy as np

data = np.load("../IMGVR/link_predict_IMGVR_sample_extra_v4_80/SkipGram_embedding_mg_imgvr_80_v4.npy")
df = pd.DataFrame(data)

print(df.shape)

df.to_csv("../IMGVR/link_predict_IMGVR_sample_extra_v4_80/SkipGram_embedding_mg_imgvr_80_v4.tsv", sep="\t")