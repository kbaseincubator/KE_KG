rm(list=ls())
setwd("~/Documents/KBase/KE/KE_KG/")

#library("pheatmap") 
#library("amap")#
#library("gplots")
#library("RColorBrewer")
#library("cluster")
#library("grid")
#library("tcR")

setwd("~/Documents/KBase/KE/KE_KG/")

data <- read.csv("../IMGVR/embeddings/SkipGram_IMGVR_merged_finalv2_kg_embedding.tsv", sep="\t", header=TRUE, row.names=1)
head(data)
dim(data)
#node_data <- read.csv("../KE_KG/data/merged_last/IMGVR_merged_final_KGX_nodes.tsv", sep="\t",header=T)
node_data <- read.csv("../KE_KG/data/merged/merged_kg_nodes.tsv", sep="\t",header=T)
dim(node_data)
head(node_data) 

#GOLD:bulk_soil

row.names(data) <- node_data$id
head(row.names(data))

grep("GOLD:human$", node_data$id)#hot_spring_water#sputum#marine_hydrothermal_vent#mouse_gut
index <- grep("GOLD:human$", node_data$id)
node_data[index,]

#write.table(data, file="../IMGVR/embeddings/SkipGram_IMGVR_merged_finalv2_kg_embedding_wids.tsv",sep="\t", row.names = F)


#row.names(data)[index]

#Alkaline = 3
queries <- index[1] #index
print(row.names(data)[queries])
for(i in 1:length(queries)) {
  print(paste("running", row.names(data)[queries[i]]))
  run_search( row.names(data)[queries[i]], data[queries[i],], data, distance="cosine", cutoff=0.9, 100)
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

run_search <- function(query, query_data, data, distance, cutoff, hits, search_string) {
  
  qindex <- which(row.names(data) == query)
  
  #print(as.numeric(query_data[qindex,]))
  
  print(paste("qindex", qindex))
  if(length(qindex) == 0) {
    return("query not found")
  }
  
  #print(paste(query, qindex))
  
  if(distance == "euclidean" && cutoff > 0.1) {
    print("WARNING: large cutoff for Euclidean distance!")
  }
  start_time <- Sys.time()
  total <- 0
  all <- c()
  
  output <- c()
  labels <- c()
  max_non_1 <- 0
  max_non_1_label <- ""
  for(j in 1:dim(data)[1]) {
    
    if(distance == "cosine") {
      #print(as.numeric(query_data))
      #print(as.numeric(data[j,]))
      dist <- cosine_simfast(as.numeric(query_data), as.numeric(data[j,]))
      #print(paste("dist cos", dist))
      if(dist != 1 && dist > max_non_1) {
        max_non_1 <- dist
        max_non_1_label <- row.names(data)[j]
        print(paste("max ", max_non_1_label, max_non_1, sep=" "))
      }
      if(dist >= cutoff) {
        print(paste("found cos ", row.names(data)[j], dist, sep=" "))
        #print(row.names(datahuman)[j])
        output <- c(output, dist)
        addval <- row.names(data)[j]#paste(query, row.names(data)[j], sep="\t")
        labels <- c(labels, addval)
        total <- total + 1
      }
    }
    else if(distance == "euclidean") {
      dist <- dist(rbind(as.numeric(query_data), as.numeric(data[j,])))
      if(dist != 0 && dist < max_non_1) {
        max_non_1 <- dist
        max_non_1_label <- row.names(data)[j]
        print(paste("min ", max_non_1_label, max_non_1, sep=" "))
      }
      if(dist <= cutoff) {
        print(paste("found euc ", row.names(data)[j], dist, sep=" "))
        #print(row.names(datahuman)[j])
        #print(paste("dist euc", dist))
        output <- c(output, dist)
        addval <-  row.names(data)[j]#paste(query,, sep="\t")
        labels <- c(labels, addval)
        total <- total +1
      }
    }
    
    #all <- c(all, as.numeric(dist))
  }
  
  names(output) <- labels
  if(length(output) >0) {
    #sort and take top hits
    sorted_top <- sort(abs(output), decreasing=TRUE)[1:min(length(output), hits)]
    print(sorted_top)
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

