library(bigmemory)
library(biganalytics)
library(bigtabulate)


setwd("/global/cfs/cdirs/kbase/ke_prototype/KE_KG/")


labels <- read.csv("./SkipGram_embedding_merged_imgvr_mg_good__cosine_labels.tsv",header=T,sep="\t")

school.matrix <- read.big.matrix(
    "./SkipGram_embedding_merged_imgvr_mg_good__cosine.tsv",header=T,sep="\t",
    type ="double", backingfile = "KG-IMGVR_cosine.bin",
    descriptorfile ="KG-IMGVR_cosine.desc", extraCols =NULL)

desc <- describe(school.matrix)

print(desc)
str(school.matrix)