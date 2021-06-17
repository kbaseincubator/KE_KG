import pandas as pd
import numpy as np
from scipy.stats import pearsonr

import time
import os

#df_taxa_orig = pd.read_csv("./MGnify/taxonomy_aggregated_full_removed_duplicates.tsv", sep="\t")
df_taxa_orig = pd.read_csv("./MGnify/go_aggregated_4.1.tsv", sep="\t", index_col=0)

print("read input")
print(df_taxa_orig.shape)
#exclude categorical

cols = [col for col in df_taxa_orig.columns if col not in ['id', 'study_id', 'sample_id', 'biome', 'exptype', 'version']]

df_taxa = df_taxa_orig[cols]
print(df_taxa.shape)

pearson_out = []
#start = time.process_time()
#last = start
#limit = 100
count = 0
for i in range(0, df_taxa.index.size):
#for col in df_taxa.columns:
    row = df_taxa.index[i]
    #colind = df_taxa.columns.index(col)
    if(len(df_taxa.loc[row][df_taxa.loc[row] > 0]) > 0):
        for j in range(i+1, df_taxa.index.size):
            # for col2 in df_taxa.columns:
            row2 = df_taxa.index[j]
            # col2ind = df_taxa.columns.index(col2)
            # print(col2)
            if (len(df_taxa.loc[row2][df_taxa.loc[row2] > 0]) > 0):

                stat, p = pearsonr(df_taxa.loc[row], df_taxa.loc[row2])

                if (count % 100 == 0):
                    print("count " + str(count))
                    print("stat, p %s %s" % (stat, p))
                    #print(df_taxa[col]+"\t"+df_taxa[col2])


                #print(df_taxa[col])
                pearson_out.append([row, row2, stat, p])
                pearson_out.append([row2, row, stat, p])

                #print("%s %s" % (stat,p))
                #curtime = time.process_time()
                #print(curtime - last)
                #last = curtime
                count = count + 1
                #if(count > limit):
                #    break

print("done pearson")
pearson_out_df = pd.DataFrame(pearson_out, columns=["row1", "row2", "pearson_stat", "pearson_pval"], dtype=np.float64)
print("done pearson df")
print(pearson_out_df.shape)

pearson_out_df.to_csv("df_GO_row_pearson.tsv", sep="\t")
print("done tsv")