
rm(list=ls())

library("plyr")

setwd("~/Documents/KBase/KE/embedding_searches/embedding-search-Jan28_IMGVR_Torben_merge")


files <- list.files("./")


data <- list()#data.frame(matrix(NA, nrow = length(files)))
count <- 1
for(i in 1:length(files)) {
  datanow <- read.csv(files[i], sep="\t")
  dimd <- dim(datanow)
  print(dimd)
  if(dimd[1] > 0) {
    print("adding")
    #data <- rbind(data, as.character(datanow[,1]))
    data[[count]] <- as.character(datanow[,1])
    #data[i,] <- datanow[,1]
    count <- count+1
  }
}
length(data)

data_unlist_all <- unlist(data)
length(data_unlist_all)

df <- do.call(rbind,lapply(data,function(x) "length<-"(x,max(lengths(data)))))
dim(df)

#df <- do.call(rbind.fill, data)
#df <- data.frame(matrix(unlist(data), nrow=length(data), byrow=T),stringsAsFactors=FALSE)




jaccard <- function(a, b) {
  intersection = length(intersect(a, b))
  union = length(a) + length(b) - intersection
  return (intersection/union)
}

dim_df <- dim(df)
pairwise_jaccard <- data.frame(matrix(NA, nrow = dim_df[1], ncol=dim_df[1]))
for(i in 1:dim_df[1]) {
  for(j in 1:dim_df[1]) {
    if(i != j) {
      pairwise_jaccard[i, j] <- jaccard(df[i,], df[j,])
    }
    else {
      pairwise_jaccard[i, j] <- 0
    }
  }
}


library(RColorBrewer)
library(ggplot2)
library(pheatmap)
library(amap)
library(gplots) 


cellwidth <- 1
cellheight <- 1
fontsize_row <- 5
fontsize_col <- 5


#pairwise_jaccard[which(pairwise_jaccard == 1)] <- 0

range <- range(pairwise_jaccard)
mypalette <- rev(brewer.pal(4, "Blues"))
mypalette <- c(mypalette, brewer.pal(4, "YlOrBr"))
breaks <- seq(0, range[2],range[2]/8)


heatmap.2(as.matrix(pairwise_jaccard), trace="none")


png(filename=paste("clustering_cosine_jaccard.png",sep=""),width=1200, height=800)
pheatmap(as.matrix(virus_host_positive),scale = "none", cluster_rows = TRUE,
         cluster_cols = TRUE, clustering_distance_rows = "euclidean",
         clustering_distance_cols = "euclidean", clustering_method = "complete",cellwidth=cellwidth,cellheight=cellheight,breaks=breaks,color=mypalette,show_rownames=F,show_colnames=F,legend=F)#
dev.off(2)


