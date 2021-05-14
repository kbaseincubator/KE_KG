

rm(list = ls())

library("plyr")
library("gplots")

#setwd("~/Documents/KBase/KE/embedding_searches/embedding-search-Feb18-run2")

setwd("/global/cfs/cdirs/kbase/ke_prototype/sean/cosine_sim_20210513")

files <- list.files("./")

names <- c()
all_names <- c()
data <- list()#data.frame(matrix(NA, nrow = length(files)))
count <- 1
lastgood <- data.frame()
for (i in 1:length(files)) {
  if (i %% 1000 == 0) {
    print(i)
  }
  datanow <- read.csv(files[i], sep = "\t")
  dimd1 <- dim(datanow)
  #print(dimd1[1])
  #print(head(datanow))
  datanow <- datanow[which(datanow[, 2] > 0.8), ]
  dimd2 <- dim(datanow)
  #print(dimd2[1])
  
  #cosine__NCBItaxon:;;;;;alphasatellitidae;;_top10000_cutoff0.1.txt
  start <- gregexpr(pattern = '__', files[i])[[1]][1]
  end <- gregexpr(pattern = '_top10', files[i])[[1]][1]
  name <- substr(files[i], start + 2, end - 1)
  #print(name)
  
  if (dimd2[1] > 0) {
    #print("adding")
    #print(dimd1[1] - dimd2[1])
    #data <- rbind(data, as.character(datanow[,1]))
    data[[count]] <- as.character(datanow[, 1])
    #print(data[[count]])
    #data[i,] <- datanow[,1]
    names <- c(names, name)
    count <- count + 1
    lastgood <- datanow
  }
  all_names <- c(all_names, name)
}

length(data)

data_unlist_all <- unlist(data)
length(data_unlist_all)

df <-
  do.call(rbind, lapply(data, function(x)
    "length<-"(x, max(lengths(
      data
    )))))
dim(df)

head(df)

#dfna <- apply(df, 1, function(x) { sum(is.na(x))})
#which(dfna == 998)

#df <- do.call(rbind.fill, data)
#df <- data.frame(matrix(unlist(data), nrow=length(data), byrow=T),stringsAsFactors=FALSE)



jaccard <- function(a, b) {
  intersection = length(intersect(a, b))
  union = length(a) + length(b) - intersection
  return (intersection / union)
}


head(df)
dim_df <- dim(df)
pairwise_jaccard <-
  data.frame(matrix(NA, nrow = dim_df[1], ncol = dim_df[1]))
for (i in 1:dim_df[1]) {
  if (i %% 10000 == 0) {
    print(i)
  }
  dfi <- df[i, ][which(!is.na(df[i, ]))]
  for (j in i:dim_df[1]) {
    dfj <- df[j, ][which(!is.na(df[j, ]))]
    if (i != j) {
      if (i > j) {
        pairwise_jaccard[i, j] <- jaccard(dfi, dfj)
        pairwise_jaccard[j, i] <- pairwise_jaccard[i, j]
        #intersect <- intersect(dfi, dfj)
        #if(length(intersect) > 0) {
        #  outf <- paste(names[i], "_", names[j],"_common.txt",sep="")
        #  print(outf)
        #  write.table(intersect, file=outf,sep="\t")
        #}
      }
    }
    else {
      pairwise_jaccard[i, j] <- 0
    }
  }
}

row.names(pairwise_jaccard) <- names
colnames(pairwise_jaccard) <- names

write.table(
  pairwise_jaccard,
  file = "pairwise_jaccard.tsv",
  sep = "\t",
  row.names = F,
  col.names = F
)
print("wrote tsv")
#write.table(names, file="GOLD_names.txt",row.names=F, col.names=F)
#write.table(names_all, file="GOLD_names_all.txt",row.names=F, col.names=F)

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
breaks <- seq(0, range[2], range[2] / 8)


#heatmap.2(as.matrix(pairwise_jaccard), trace="none")#log(pairwise_jaccard + 0.001, 10))




png(
  filename = paste("clustering_cosine_jaccard_0.8.png", sep = ""),
  width = 1200,
  height = 800
)
pheatmap(
  as.matrix(virus_host_positive),
  scale = "none",
  cluster_rows = TRUE,
  cluster_cols = TRUE,
  clustering_distance_rows = "euclidean",
  clustering_distance_cols = "euclidean",
  clustering_method = "complete",
  cellwidth = cellwidth,
  cellheight = cellheight,
  breaks = breaks,
  color = mypalette,
  show_rownames = F,
  show_colnames = F,
  legend = F
)#
dev.off(2)
