library(RColorBrewer)
library(ggplot2)
library(pheatmap)
library(amap)
library(gplots) 

rm(list=ls())

setwd("~/Documents/KBase/KE/IMGVR/")
node_data <- read.csv("./merged_imgvr_mg_nodes.tsv", sep="\t",header=T)

dim(node_data)
#head(node_data) 

node_labels <- as.character(node_data$id)


embeddings <- read.csv("./embeddings/SkipGram_merged_imgvr_mg_embedding.tsv", sep="\t", header=TRUE, row.names=1)
head(embeddings)
dim(embeddings)


#virus_host_positive <- read.csv("./link_predict/virus_host__subtract.tsv", row.names=1)
virus_host_positive <- read.csv("./link_predict/virus_host__subtract.tsv", row.names=1, header=TRUE, sep=",")
virus_host_positive_labels <- read.csv("./link_predict/virus_host__subtract_labels.tsv")
dim(virus_host_positive)
dim(virus_host_positive_labels)
#head(virus_host_positive)
dimpos <- dim(virus_host_positive)
dimpos



virus_host_negative <- read.csv("./link_predict/virus_host_NEGATIVE__subtract.tsv", row.names=1, header=TRUE, sep=",")
virus_host_negative_labels <- read.csv("./link_predict/virus_host_NEGATIVE__subtract_labels.tsv")
dim(virus_host_negative)
sum(is.na(virus_host_negative))
dim(virus_host_negative_labels)
#head(virus_host_negative)
dimneg <- dim(virus_host_negative)
#head(virus_host_negative)
row.names(virus_host_negative) <- virus_host_negative_labels[,1]


virus_host_new <- read.csv("./link_predict/virus_host_NEW__subtract.tsv", row.names=1, header=TRUE, sep=",")
virus_host_new_labels <- read.csv("./link_predict/virus_host_NEW_subtract_labels.tsv")
dim(virus_host_new)
sum(is.na(virus_host_new))
dim(virus_host_new_labels)
#head(virus_host_new)
dimnew <- dim(virus_host_new)
#head(virus_host_new)
row.names(virus_host_new) <- virus_host_new_labels[,1]


cellwidth <- 1
cellheight <- 1
fontsize_row <- 5
fontsize_col <- 5

range(virus_host_positive)
mypalette <- rev(brewer.pal(4, "Blues"))
mypalette <- c(mypalette, brewer.pal(4, "YlOrBr"))
breaks <- seq(-31, 29,35)


heatmap.2(as.matrix(virus_host_positive), trace="none")


png(filename=paste("clustering_positive.png",sep=""),width=1200, height=800)
pheatmap(as.matrix(virus_host_positive),scale = "none", cluster_rows = TRUE,
         cluster_cols = TRUE, clustering_distance_rows = "euclidean",
         clustering_distance_cols = "euclidean", clustering_method = "complete",cellwidth=cellwidth,cellheight=cellheight,breaks=breaks,color=mypalette,show_rownames=F,show_colnames=F,legend=F)#
dev.off(2)
