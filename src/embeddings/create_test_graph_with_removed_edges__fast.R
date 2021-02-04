
rm(list=ls())

library("randomForest")
library("caTools")
library ("ROCR")
library("data.table")
library("plyr")
library("hash")
#library("fmatch")

#setwd("~/graphs/KE_KG")
#node_data <- read.csv("/global/cfs/cdirs/kbase/ke_prototype/KE_KG/data/merged/merged_imgvr_mg_nodes.tsv", sep="\t",header=T)
setwd("~/Documents/KBase/KE/IMGVR/")
node_data <- read.csv("./IMGVR_merged_kg_nodes.tsv", sep="\t",header=T)
edge_data <- read.csv("./IMGVR_merged_kg_edges.tsv", sep="\t",header=T)

dim(node_data)
dim(edge_data)
head(edge_data)
head(node_data)

#head(node_data) 

node_labels <- as.character(node_data$id)

test_edges <- read.csv("IMGVR_sample_extra_test_edges.txt", row.names=1, header=TRUE, sep="\t")
class(test_edges)
test_edges[,1]
test_edges_split <- strsplit(as.character(test_edges[,1]), "__", fixed=TRUE)
test_edges_split_mat <- unlist(test_edges_split)
head(test_edges_split_mat)

#grep(node2, edge_data[,'subject'])


subjsplit_raw <- unlist(test_edges_split)[2*(1:length(test_edges_split))-1]
head(subjsplit_raw)
subjsplit <- unlist(strsplit(as.character(subjsplit_raw), "\t", fixed=TRUE))[2*(1:length(test_edges_split))]
head(subjsplit)
objsplit  <- unlist(test_edges_split)[2*(1:length(test_edges_split))  ]
head(objsplit)

all_edges_str <- paste(edge_data[,'subject'], "__",edge_data[,'object'], sep="")
head(all_edges_str)
test_edges_str <- paste(objsplit, "__",subjsplit, sep="")
head(test_edges_str)

all_edges_minus_test_index <- match(all_edges_str ,test_edges_str)


new_edges <- edge_data[which(is.na(all_edges_minus_test_index)), ]
new_nodes <- node_data[which(is.na(all_edges_minus_test_index)), ]
#colnames(new_edges) <- c("uuid", "subject", "predicate", "object", "source")
#colnames(new_nodes) <- c("id", "label", "category", "source")
write.table(new_edges, file="./IMGVR_merged_kg_edges__positive80.tsv", sep="\t", row.names=FALSE)
write.table(new_nodes, file="./IMGVR_merged_kg_nodes__positive80.tsv", sep="\t", row.names=FALSE)


