import modin.pandas as pd
import numpy as np
import seaborn as sns
import os

df_taxa_orig = pd.read_csv("../../../MGnify/taxonomy_aggregated_full_removed_duplicates.tsv", sep="\t")

cols = [col for col in df_taxa_orig.columns if col not in ['id', 'study_id', 'sample_id', 'biome', 'exptype']]
#df_taxa = df_taxa_orig[df_taxa_orig.columns.difference(['id', 'study_id', 'sample_id', 'biome', 'exp_type'])]
df_taxa = df_taxa_orig[cols]
df_taxa.shape

df_taxa_colsums = df_taxa.sum(axis=0)

df_taxa_colsums.to_csv("df_taxa_colsums.tsv", sep="\t")

df_taxa_colsums[df_taxa_colsums > 0]

#new_df = pd.DataFrame(df_taxa_colsums[df_taxa_colsums > 0], columns=["X"])
new_df = pd.DataFrame(df_taxa_colsums, columns=["X"])
#new_df.iloc[0:100]
new_df.shape


histplot = sns.histplot(data=new_df,x='X', log_scale=True)
fig = histplot.get_figure()
fig.savefig("histplot.png")
histplot

