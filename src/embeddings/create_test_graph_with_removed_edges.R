
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

cur_edges <- paste(edge_data[,'subject'], "__",edge_data[,'object'], sep="")
head(cur_edges)



test_edges_clean <- c()
for(i in 1:length(test_edges_split)){
  curedge <- unlist(test_edges_split[i])
  node1 <- unlist(strsplit(curedge[1], "\t"))[2]
  node2 <- curedge[2]
  testedge <- paste(node2, "__", node1, sep="")
  test_edges_clean <- c(test_edges_clean, testedge)
}
head(test_edges_clean)
length(test_edges_clean)



new_edges <-  data.frame(matrix(ncol = 6, nrow = length(cur_edges)))#vector(mode="character", length=length(cur_edges))#
colnames(new_edges) <- colnames(edge_data)#"subject\tpredicate\tobject"
new_nodes <- data.frame(matrix(ncol = 4, nrow = length(node_labels)))#ector(mode="character", length=length(node_labels))
colnames(new_nodes) <-  colnames(node_data)#"id\tlabel\tcategory"
new_nodes_labels <- vector(mode="character", length=length(node_labels))#c()
edgecount <- 0
nodecount <- 0
head(cur_edges)
head(test_edges_clean)
cur_edges_index <- match(cur_edges, test_edges_clean)
head(cur_edges_index)
length(cur_edges_index)
sum(is.na(cur_edges_index))
class(cur_edges)
cur_edges_split <- strsplit(cur_edges, "__")#sapply(cur_edges, function(x) strsplit(x, "__")[[1]], USE.NAMES=FALSE)#ldply(
length(cur_edges_split)
#length(cur_edges)
subjsplit    <- unlist(cur_edges_split)[2*(1:length(cur_edges_split))-1]
head(subjsplit)
objsplit  <- unlist(cur_edges_split)[2*(1:length(cur_edges_split))  ]
head(objsplit)
cur_edges_split_df <- data.frame(cbind(as.character(subjsplit), as.character(objsplit)),stringsAsFactors = F)

class(node_labels)
node_label_hash <- hash( keys=node_labels, values=1:length(node_labels))
head(node_label_hash)
unlist(as.list(node_label_hash["vOTU:sg_502237"]))
match("vOTU:sg_502237", node_labels)
has.key("vOTU:sg_502237", node_label_hash)
head(unlist(as.list(node_label_hash)))
head(keys(node_label_hash))

#edge_data_filtered <- edge_data
for(i in 1:length(cur_edges)) {
  if( i %% 100 == 0) {
    print(i)
  }
  #if(!(cur_edges[i] %chin% test_edges_clean)) {
  if(is.na(cur_edges_index[i])) {
    #split <- strsplit(cur_edges[i], "__")
    #split1 <- unlist(split)[1]#,"\t")[2]
    #split2 <- unlist(split)[2]#,"\t")[2]
    new_edges[edgecount,] <- edge_data[i,]#addedge
    edgecount <- edgecount +1
    n1 <- cur_edges_split_df[i, 1]
    n2 <- cur_edges_split_df[i, 2]
    
    if(!(n1 %chin% new_nodes_labels)) {
      ind1 <- as.numeric(unlist(as.list(node_label_hash[n1]))[1])#node_label_hash[n1]#chmatch(n1, node_labels)
      new_nodes[nodecount,] <- node_data[ind1,]
      new_nodes_labels[nodecount] <- n1
      nodecount <- nodecount+1
    }
    if(!(n2 %chin% new_nodes_labels)) {
      ind2 <-  as.numeric(unlist(as.list(node_label_hash[n2]))[1])#node_label_hash[n2]#ind2 <- chmatch(n2, node_labels) 
      new_nodes[nodecount,] <- node_data[ind2,]
      new_nodes_labels[nodecount] <- n2
      nodecount <- nodecount+1
    }
  }
}
#new_nodes <- new_nodes[-1,]
dim(new_edges)
dim(new_nodes)
length(node_labels)

print(edge_data[1,])


write.table(new_edges, file="./IMGVR_merged_kg_edges__positive80.tsv", sep="\t", row.names=FALSE, col.names=FALSE)
write.table(new_edges, file="./IMGVR_merged_kg_nodes__positive80.tsv", sep="\t", row.names=FALSE, col.names=FALSE)



