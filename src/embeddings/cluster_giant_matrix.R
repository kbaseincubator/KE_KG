
library(RColorBrewer)
library(ggplot2)
library(pheatmap)

setwd("/global/cfs/cdirs/kbase/ke_prototype/KE_KG/")


data <- read.csv("./SkipGram_embedding_merged_imgvr_mg_good__cosine.tsv",header=T,sep="\t")
labels <- read.csv("./SkipGram_embedding_merged_imgvr_mg_good__cosine_labels.tsv",header=T,sep="\t")
head(data)
print(paste("dim ",dim(data))
range <- range(data)
print(paste("range ",range))

mypalette <- rev(brewer.pal(5, "Blues"))[1]
mypalette <- c(mypalette, brewer.pal(5, "YlOrBr"))

cellwidth <- 2
cellheight <- 2
fontsize_row <- 6
fontsize_col <- 6


breaks <- seq(range[1],range[2],(range[2]-range[1])/10)


png("cluster_giant.png",height=6000, width=1000)
pheatmap(as.matrix(data), cluster_rows=T, cluster_cols=T, cellwidth=cellwidth,cellheight=cellheight,breaks=breaks,color=mypalette,show_rownames=T,show_colnames=T,legend=T,
         fontsize_row=fontsize_row,fontsize_col=fontsize_col)
dev.off(2)