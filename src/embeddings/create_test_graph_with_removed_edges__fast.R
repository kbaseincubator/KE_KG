
rm(list=ls())

set.seed(12345)

library("randomForest")
library("caTools")
library ("ROCR")
library("data.table")
library("plyr")
library("hash")
#library("fmatch")

setwd("~/Documents/KBase/KE/IMGVR/")

node_data <- read.csv("./merged_imgvr_mg_nodes_good.tsv", sep="\t",header=T)
edge_data <- read.csv("./merged_imgvr_mg_edges_good.tsv", sep="\t",header=T)


#node_data <- read.csv("./link_predict_mg_imgvr_OPT_v5_noko/merged_imgvr_mg_nodes_good_noko_whead.tsv", sep="\t",header=T)
#edge_data <- read.csv("./link_predict_mg_imgvr_OPT_v5_noko/merged_imgvr_mg_edges_good_noko_whead.tsv", sep="\t",header=T)


#setwd("~/Documents/VIMSS/ontology/KG-Hub/KG-Microbe/")
#edge_data <- read.csv("./20210315/merged-kg/merged-kg_edges.tsv", sep="\t",header=T, quote="", stringsAsFactors = FALSE)
#node_data <- read.csv("./20210315/merged-kg/merged-kg_nodes.tsv", sep="\t",header=T, quote="", stringsAsFactors = FALSE)

dim(node_data)
dim(edge_data)
head(edge_data)
head(node_data)

#head(node_data) 

node_labels <- as.character(node_data$id)

#test_edges <- read.csv("IMGVR_sample_extra_test_edges.txt", row.names=1, header=TRUE, sep="\t")
#dim(test_edges)
#class(test_edges)
#test_edges[,1]
#test_edges_split <- strsplit(as.character(test_edges[,1]), "__", fixed=TRUE)
#test_edges_split_mat <- unlist(test_edges_split)
#head(test_edges_split_mat)


test_data <- read.csv("./link_predict_mg_imgvr_OPT_v5/IMGVR_test.txt", row.names=1, header=TRUE, sep="\t")
#test_data <- read.csv("./link_predict_mg_imgvr_OPT_v5_noko/IMGVR_sample_extra_test.txt", row.names=1, header=TRUE, sep="\t")
#test_data <- read.csv("./link_predict_kgmicrobe_shape/kgmicrobe_test.txt", row.names=1, header=TRUE, sep="\t")
dim(test_data)
head(test_data)
row.names(test_data)

train_data <- read.csv("./link_predict_mg_imgvr_OPT_v5/IMGVR_train.txt", row.names=1, header=TRUE, sep="\t")
#train_data <- read.csv("./link_predict_mg_imgvr_OPT_v5_noko/IMGVR_sample_extra_train.txt", row.names=1, header=TRUE, sep="\t")
#train_data <- read.csv("./link_predict_kgmicrobe_shape/kgmicrobe_train.txt", row.names=1, header=TRUE, sep="\t")
dim(train_data)

#grep(node2, edge_data[,'subject'])

test_edges_split <- strsplit(row.names(test_data), "__")
subjsplit_raw <- unlist(test_edges_split)[2*(1:length(test_edges_split))-1]
head(subjsplit_raw)
subjsplit <- unlist(strsplit(as.character(subjsplit_raw), "\t", fixed=TRUE))[2*(1:length(test_edges_split))]
head(subjsplit)
objsplit  <- unlist(test_edges_split)[2*(1:length(test_edges_split))  ]
head(objsplit)

all_edges_str <- paste(edge_data[,'subject'], "__",edge_data[,'object'], sep="")
head(all_edges_str)
head(test_data)
#test_edges_str <- paste(test_data[,'subject'], "__",test_data[,'object'], sep="")
test_edges_str <- paste(objsplit, "__",subjsplit, sep="")
head(test_edges_str)

all_edges_minus_test_index <- match(all_edges_str ,test_edges_str)


sum(is.na(all_edges_minus_test_index))


new_edges <- edge_data[which(is.na(all_edges_minus_test_index)), ]
hold_edges_20 <- which(is.na(all_edges_minus_test_index))

new_node_ids <- unique(c(as.vector(new_edges[,'subject']),as.vector(new_edges[,'object'])))
length(new_node_ids)
head(new_node_ids)
new_node_index <- match(new_node_ids, node_labels)
new_nodes <- node_data[new_node_index, ]
dim(new_nodes)
hold_nodes_20 <- which(is.na(match(node_labels, new_node_ids)))

#colnames(new_edges) <- c("uuid", "subject", "predicate", "object", "source")
#colnames(new_nodes) <- c("id", "label", "category", "source")
write.table(new_edges, file="./IMGVR_merged_kg_edges__positive80.tsv", sep="\t", row.names=FALSE, quote=FALSE)
write.table(hold_edges_20, file="./IMGVR_merged_kg_edges__positive20_index.tsv", sep="\t", row.names=FALSE, col.names=FALSE, quote=FALSE)
write.table(new_nodes, file="./IMGVR_merged_kg_nodes__positive80.tsv", sep="\t", row.names=FALSE, quote=FALSE)
write.table(hold_nodes_20, file="./IMGVR_merged_kg_nodes__positive20_index.tsv", sep="\t", row.names=FALSE, col.names=FALSE, quote=FALSE)


