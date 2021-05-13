import modin.pandas as pd
import numpy as np
import seaborn as sns
from scipy.stats import shapiro

import time
import os

df_taxa_orig = pd.read_csv("../../../MGnify/taxonomy_aggregated_full_removed_duplicates.tsv", sep="\t")

cols = [col for col in df_taxa_orig.columns if col not in ['id', 'study_id', 'sample_id', 'biome', 'exptype']]
df_taxa = df_taxa_orig[cols]
df_taxa.shape


shapiro_out = []
start = time.process_time()
last = start
limit = 100
count = 0
for col in df_taxa.columns:
    #print(col)
    stat, p = shapiro(df_taxa[col])
    #print(df_taxa[col])
    shapiro_out.append([stat,p])
    #print("%s %s" % (stat,p))
    #curtime = time.process_time()
    #print(curtime - last)
    #last = curtime
    #count = count +1
    #if(count > limit):
    #    break

shapiro_out_df = pd.DataFrame(shapiro_out, columns=["stat", "p"], dtype=np.float64)
shapiro_out_df.shape

shapiro_out_df.to_csv("df_taxa_col_shapiro.tsv", sep="\t")