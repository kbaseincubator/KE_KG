library(RColorBrewer)
library(ggplot2)
library(pheatmap)

library(bigmemory)
library(biganalytics)
library(bigtabulate)

setwd("/global/cfs/cdirs/kbase/ke_prototype/KE_KG/")


dist_all  <- read.big.matrix(
    "./SkipGram_embedding_merged_imgvr_mg_good__cosine.tsv",header=T,sep="\t",
    type ="double", backingfile = "KG-IMGVR_cosine.bin",
    descriptorfile ="KG-IMGVR_cosine.desc", extraCols =NULL)

#png("cluster_giant.png",height=6000, width=1000)
centers <- 100
bigkm <- bigkmeans(dist_all, centers, iter.max = 10, nstart = 1, dist = "euclid")
#dev.off(2)

write(bigkm, "bigkm.txt")