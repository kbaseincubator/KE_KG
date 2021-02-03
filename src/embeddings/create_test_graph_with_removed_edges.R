rm(list=ls())

library("randomForest")
library("caTools")
library ("ROCR")

setwd("~/graphs/KE_KG")
node_data <- read.csv("/global/cfs/cdirs/kbase/ke_prototype/graphs/IMGVR/sample_extra/IMGVR_merged_kg_nodes.tsv", sep="\t",header=T)
edge_data <- read.csv("/global/cfs/cdirs/kbase/ke_prototype/graphs/IMGVR/sample_extra/IMGVR_merged_kg_edges.tsv", sep="\t",header=T)

dim(node_data)
dim(edge_data)
head(edge_data)
head(node_data)

#head(node_data) 

node_labels <- as.character(node_data$id)

test_edges <- read.csv("/global/cfs/cdirs/kbase/ke_prototype/graphs/IMGVR/sample_extra/IMGVR_sample_extra_test_edges.txt", row.names=1, header=TRUE, sep="\t")
class(test_edges)
test_edges[,1]
test_edges_split <- strsplit(as.character(test_edges[,1]), "__", fixed=TRUE)
test_edges_split_mat <- unlist(test_edges_split)
head(test_edges_split_mat)

grep(node2, edge_data[,'subject'])

cur_edges <- paste(edge_data[,'subject'], "__",edge_data[,'object'], sep="")
head(cur_edges)



test_edges_clean <- c()
for(i in 1:length(test_edges_split)){
  curedge <- unlist(test_edges_split[i])
  node1 <- unlist(strsplit(curedge[1], "\t"))[2]
  node2 <- curedge[2]
  testedge <- paste(node1, "__", node2, sep="")
  test_edges_clean <- c(test_edges_clean, testedge)
}
head(test_edges_clean)
length(test_edges_clean)

new_edges <- "subject\tpredicate\tobject"
new_nodes <- "id\tlabel\tcategory"
new_nodes_labels <- c()
#edge_data_filtered <- edge_data
for(i in 1:length(cur_edges)) {
	if( i %% 100 == 0) {
	   print(i)	
	}
  oldedge <- cur_edges[i]
  ind1 <- match(oldedge, test_edges_clean)
  if(is.na(ind1)) {
    split <- strsplit(oldedge, "__")
    split1 <- unlist(split)[1]#,"\t")[2]
    split2 <- unlist(split)[2]#,"\t")[2]
    addedge <-  paste(split1, "\tbiolink:has_attribute\t", split2, sep="")
    new_edges <- c(new_edges,edge_data) 
    #print(addedge)
    if(is.na(match(split1, new_nodes_labels))) {
      ind1 <- match(split1, node_labels)
      new_nodes <- rbind(new_nodes, node_data[ind1,]) 
    }
    if(is.na(match(split2, new_nodes_labels))) {
      ind2 <- match(split2, node_labels)
      new_nodes <- rbind(new_nodes, node_data[ind2,])  
    }
  }
}
new_nodes <- new_nodes[-1,]
length(new_edges)
length(new_nodes)

write.table(new_edges, file="./IMGVR_merged_kg_edges__positive80.tsv", sep="\t", row.names=FALSE, header=FALSE)
write.table(new_edges, file="./IMGVR_merged_kg_nodes__positive80.tsv", sep="\t", row.names=FALSE, header=FALSE)



