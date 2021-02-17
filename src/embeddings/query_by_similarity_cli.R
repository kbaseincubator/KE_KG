#!/usr/bin/env Rscript

rm(list=ls())

# load argparse first because needed to check for input files
library("argparse")

# create parser object
parser <- ArgumentParser()

parser$add_argument("-e", "--embeddings", help="Indicate an embeddings file", default="")
parser$add_argument("-n", "--nodes", help="Indicate a nodes file", default="")
parser$add_argument("-s", "--search_string", help="Search term (e.g. GOLD:anaerobic, GOLD:bulk_soil, ...)", default="")
parser$add_argument("-w", "--working_directory", help="Indicate working directory", default=getwd())
parser$add_argument("-d", "--distance", help="Indicate distance method [cosine|euclidean] (default: cosine)", default="cosine")
parser$add_argument("-c", "--cutoff", help="Indicate cutoff value (default: 0.85)", default=0.9)
parser$add_argument("-z", "--num_hits", help="Indicate number of hits to retain and export (default: 1000)", default=1000)

# get command line options, if help option encountered print help and exit,
# otherwise if options not found on command line then set defaults,
args <- parser$parse_args()


# print some progress messages if variables not entered correctly
if ( args$embeddings == "" ) {
    write("Error: bad link to embeddings file. Exiting.\n", stderr())
    quit(status=1)
}

if ( args$nodes == "" ) {
    write("Error: bad link to nodes file. Exiting.\n", stderr())
    quit(status=1)
}

if ( args$search_string == "" ) {
    write("Error: input a search string. Exiting.\n", stderr())
    quit(status=1)
}

if (( !args$distance == "cosine" ) & ( !args$distance == "euclidean" )) {
    write("Error: incorrect distance method selected. Exiting.\n", stderr())
    quit(status=1)
}

if (( args$cutoff >= 1 ) || ( args$cutoff <= 0 )) {
    write("Error: incorrect cutoff selected. Exiting.\n", stderr())
    quit(status=1)
}

# not sure why this variable assertion isn't working, will need to address later
# if ( args$num_hits <= 0 || all.equal(args$num_hits, as.integer(args$num_hits)) != TRUE ) {
#     write("Error: incorrect number of hits selected. Exiting.\n", stderr())
#     quit(status=1)
# }

# load non-argparse libraries only after checking for required input files
#library("pheatmap")
#library("amap")
#library("gplots")
#library("RColorBrewer")
#library("cluster")
#library("grid")
#library("tcR")

embedding_file <- args$embeddings
nodes_file <- args$nodes
search_string <- args$search_string
#distance <- "cosine"
#cutoff <- 0.9
#hits <- 1000
distance <- args$distance
cutoff <- as.numeric(args$cutoff) # if not forced to a numeric type then the script will run but not respect cutoff input cutoff values
hits <- as.numeric(args$num_hits)

setwd(args$working_directory)

#embedding_file <- "/global/cfs/cdirs/kbase/ke_prototype/embeddings/SkipGram_embedding_IMGVR_merged_final_embedding.tsv"
#data <- read.csv("/global/cfs/cdirs/kbase/ke_prototype/embeddings/SkipGram_embedding_IMGVR_merged_final_embedding.tsv", sep="\t", header=TRUE, row.names=1)
data <- read.csv(embedding_file, sep="\t", header=T, row.names=1, stringsAsFactors=FALSE, quote="")
head(data)
dimdata <- dim(data)

if(dimdata[2] == 0) {
  data <- read.csv(embedding_file, sep=",", header=T, row.names=1, stringsAsFactors=FALSE, quote="")
  head(data)
  dimdata <- dim(data)
}


#nodes_file <- "/global/cfs/cdirs/kbase/ke_prototype/graphs/IMGVR/IMGVR_merged_final_KGX_nodes.tsv"
#node_data <- read.csv("/global/cfs/cdirs/kbase/ke_prototype/graphs/IMGVR/IMGVR_merged_final_KGX_nodes.tsv", sep="\t",header=T)
node_data <- read.csv(nodes_file, sep="\t",header=T, stringsAsFactors=FALSE, quote="")
dim(node_data)
head(node_data)

row.names(data) <- node_data$id

#search_string<-"GOLD:bulk_soil"
search_string_input<-paste0(search_string,'$')

#grep("GOLD:anaerobic$", node_data$id)
grep(search_string_input, node_data$id)
index <- grep(search_string_input, node_data$id)

node_data[index,]


#write.table(data, file="../IMGVR/SkipGram_embedding_IMGVR_extra_wids.tsv",sep="\t", row.names = F)

#Alkaline = 3

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
      print(paste(dist, cutoff))
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
    print("sorted_top")
    print(head(sorted_top))

    output_data<-data.frame(V1=rownames(data.frame(sorted_top)),V2=as.vector(sorted_top))

    # need next line only if output file name cannot have colon ':' symbol
    #query_output_name<-gsub(":", "_", query_output_name)
    query_output_name<-search_string

    for(i in 1:nrow(output_data)) {
      output_data$V1[i]<-node_data[as.integer(output_data$V1[i])+1,]$id
    }

    outfile <- paste(distance,"__",query_output_name,"_top",hits,"_cutoff",cutoff,".txt",sep="")

    print(paste("saving ", dim(sorted_top), outfile))

    write.table(sorted_top, outfile, sep="\t", col.names=F)
    #write.table(output_data, outfile, sep="\t", col.names=F, row.names=F, quote=F)
  }
  else {
    print("nothing")
  }

  end_time <- Sys.time()
  print(paste("time", end_time - start_time))
}

queries <- index[1] #index
print(row.names(data)[queries])
for(i in 1:length(queries)) {
  print(paste("running", row.names(data)[queries[i]]))
  #run_search( row.names(data)[queries[i]], data[queries[i],], data, distance="cosine", cutoff=0.85, hits = 1000)
  run_search( row.names(data)[queries[i]], data[queries[i],], data, distance, cutoff, hits, search_string)
}
