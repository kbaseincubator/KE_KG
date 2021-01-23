rm(list=ls())
setwd("~/Documents/KBase/KE/KE_KG/")

library("pheatmap") 
library("amap")
library("gplots")
library("RColorBrewer")
library("cluster")
library("grid")
library("tcR")

setwd("~/Documents/KBase/KE/KE_KG/")

data <- read.csv("../IMGVR/SkipGram_embedding_IMGVR_merged.tsv", sep="\t", header=TRUE, row.names=1)
head(data)
dim(data)
node_data <- read.csv("../IMGVR/IMGVR_merged_kg_nodes.tsv", sep="\t",header=T)
dim(node_data)
head(node_data) 

#GOLD:bulk_soil

row.names(data) <- node_data$id

grep("GOLD:anaerobic$", node_data$id)
index <- grep("GOLD:anaerobic$", node_data$id)
node_data[index,]

#write.table(data, file="../IMGVR/SkipGram_embedding_IMGVR_extra_wids.tsv",sep="\t", row.names = F)


#row.names(data)[index]

#Alkaline = 3
queries <- index[1] #index
print(row.names(data)[queries])
for(i in 1:length(queries)) {
  print(paste("running", row.names(data)[queries[i]]))
  run_search( row.names(data)[queries[i]], data[queries[i],], data, distance="cosine", cutoff=0.85)
}



###
###
###
cosine_simfast <- function(a,b) {
  crossprod(a,b)/sqrt(crossprod(a)*crossprod(b))
}

###for matrix
cos_sim_mat <- function(x) {crossprod(x)/(sqrt(tcrossprod(colSums(x^2))))}

angle <- function(x,y){
  dot.prod <- x%*%y 
  norm.x <- norm(x,type="2")
  norm.y <- norm(y,type="2")
  theta <- acos(dot.prod / (norm.x * norm.y))
  as.numeric(theta)
}

run_search <- function(query, query_data, data, distance="cosine", cutoff=0.9, hits = 1000) {
  
  qindex <- which(row.names(query_data) == query)
  
  print(as.numeric(query_data[qindex,]))
  
  print(paste("qindex", qindex))
  if(length(qindex) == 0) {
    return("query not found")
  }
  
  print(paste(query, qindex))
  
  if(distance == "euclidean" && cutoff == 0.9) {
    print("resetting distance cutoff for Euclidean to 0.1")
    cutoff = 0.1
  }
  start_time <- Sys.time()
  total <- 0
  all <- c()
  
  output <- c()
  labels <- c()
  for(j in 1:dim(data)[1]) {
    
    if(j != qindex) {
      if(distance == "cosine") {
        #dist <- angle(as.numeric(data[qindex,]), as.numeric(data[j,]))
        
        #print(as.numeric(data[j,]))
        dist <- cosine_simfast(as.numeric(query_data[qindex,]), as.numeric(data[j,]))
        #print(paste("dist cos", dist))
        if(dist > cutoff) {
          #print(row.names(datahuman)[j])
          output <- c(output, dist)
          addval <- row.names(data)[j]#paste(query, row.names(data)[j], sep="\t")
          labels <- c(labels, addval)
          total <- total + 1
        }
      }
      else if(distance == "euclidean") {
        dist <- dist(rbind(as.numeric(query_data[qindex,]), as.numeric(data[j,])))
        if(dist < cutoff) {
          #print(row.names(datahuman)[j])
          #print(paste("dist euc", dist))
          output <- c(output, dist)
          addval <-  row.names(data)[j]#paste(query,, sep="\t")
          labels <- c(labels, addval)
          total <- total +1
        }
      }
      
      all <- c(all, as.numeric(dist))
      
    }
  }
  
  names(output) <- labels
  if(length(output) >0) {
    #sort and take top hits
    sorted_top <- sort(abs(output), decreasing=TRUE)[1:min(length(output), hits)]
    #print(sorted_top)
    outfile <- paste(distance,"__",query,"_top",hits,"_cutoff",cutoff,".txt",sep="")
    
    print(paste("saving ", dim(sorted_top), outfile))
    write.table(sorted_top, outfile, sep="\t", col.names=F)
  }
  else {
    print("nothing")
  }
  
  end_time <- Sys.time()
  print(paste("time", end_time - start_time))
}

