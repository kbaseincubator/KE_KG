import pandas as pd
import numpy as np
from scipy.stats import pearsonr

import time
import os

df_taxa_orig = pd.read_csv("./MGnify/taxonomy_aggregated_full_removed_duplicates_col100.tsv", sep="\t")

print("read input")

#exclude categorical
cols = [col for col in df_taxa_orig.columns if col not in ['id', 'study_id', 'sample_id', 'biome', 'exptype']]
df_taxa = df_taxa_orig[cols]
print(df_taxa.shape)

pearson_out = []
#start = time.process_time()
#last = start
#limit = 100
count = 0
for i in range(0, df_taxa.columns.size):
#for col in df_taxa.columns:
    col = df_taxa.columns[i]
    #colind = df_taxa.columns.index(col)
    if(len(df_taxa[col][df_taxa[col] > 0]) > 0):
        for j in range(i+1, df_taxa.columns.size):
            # for col2 in df_taxa.columns:
            col2 = df_taxa.columns[j]
            # col2ind = df_taxa.columns.index(col2)
            # print(col2)
            if (len(df_taxa[col2][df_taxa[col2] > 0]) > 0):

                stat, p = pearsonr(df_taxa[col], df_taxa[col2])

                if (count % 100 == 0):
                    print("count " + str(count))
                    print("stat, p %s %s" % (stat, p))
                    #print(df_taxa[col]+"\t"+df_taxa[col2])


                #print(df_taxa[col])
                pearson_out.append([i, j, stat, p])
                pearson_out.append([j, i, stat, p])

                #print("%s %s" % (stat,p))
                #curtime = time.process_time()
                #print(curtime - last)
                #last = curtime
                count = count + 1
                #if(count > limit):
                #    break

print("done pearson")
pearson_out_df = pd.DataFrame(pearson_out, columns=["col1", "col2", "pearson_stat", "pearson_p"], dtype=np.float64)
print("done pearson df")
print(pearson_out_df.shape)

pearson_out_df.to_csv("df_taxa_col_pearson.tsv", sep="\t")
print("done tsv")