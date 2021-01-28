rm(list=ls())
setwd("~/Documents/KBase/KE/IMGVR/")

embeddings <- read.csv("./embeddings/SkipGram_merged_imgvr_mg_embedding.tsv", sep="\t", header=TRUE, row.names=1)
head(embeddings)
dim(embeddings)
#node_data <- read.csv("../KE_KG/data/merged_last/IMGVR_merged_final_KGX_nodes.tsv", sep="\t",header=T)
node_data <- read.csv("./merged_imgvr_mg_nodes.tsv", sep="\t",header=T)
dim(node_data)
head(node_data) 

node_labels <- as.character(node_data$id)


virus_host <- read.csv("./IMGVR_all_Sequence_information_InIMG-Yes_Linked-to_TaxonOIDs_v2_Completeness-50-100_nocol20_v1.tsv",sep="\t",header=T)
dim(virus_host)
head(virus_host) 


vOTUs <- paste("vOTU:",tolower(virus_host$vOTU),sep="")
length(vOTUs)
class(virus_host$Host_taxonomy_prediction[1])
length(virus_host$Host_taxonomy_prediction[1])
hlens <- nchar(as.character(virus_host$Host_taxonomy_prediction))#unlist(lapply(virus_host$Host_taxonomy_prediction, length))#lengths(virus_host$Host_taxonomy_prediction)
sum(hlens>1)
#virus_host$Host_taxonomy_prediction[hlens>1]

virus_host$Host_taxonomy_prediction <- gsub(" ","_",virus_host$Host_taxonomy_prediction)
hosts <- paste("NCBItaxon:",tolower(unique(virus_host$Host_taxonomy_prediction[hlens>1])),sep="")
#hosts_full <- paste("NCBItaxon:",tolower(virus_host$Host_taxonomy_prediction[hlens>1]),sep="")
#hosts <- gsub(" ","_",hosts)
length(hosts)
class(node_labels[1])

grep("vOTU:votu_219688", node_labels)
#vOTUs_index <- vOTUs %in% node_labels
#hosts_index <- hosts %in% node_labels
vOTUs_index <- match(vOTUs, node_labels)
hosts_index <- match(hosts, node_labels)

length(unique(hosts))
sum(!is.na(hosts_index))
sum(is.na(hosts_index))
hosts[is.na(hosts_index)][1:10]

host_curie <- paste("NCBItaxon:",tolower(virus_host$Host_taxonomy_prediction),sep="")


virus_host__subtract <- c()
virus_host__subtract_label <- c()


for(i in 1:length(vOTUs_index)){
  
  curhost <- host_curie[i]
  #print(curhost)
  hashost <- curhost %in% hosts
  #print(hashost)
  if(hashost) {
    if(i %% 100 == 0) {
      print(i)
    }
    hindex <- which(hashost)
    v_embed <- embeddings[vOTUs_index[i],]
    #for(j in 1:length(hosts_index)){
    h_embed <- embeddings[hosts_index[hindex],]
    
    vh_embed <- v_embed - h_embed 
    virus_host__subtract <- rbind(virus_host__subtract, vh_embed)
    
    virus_host__subtract_label <- paste(node_labels[vOTUs_index[i]],"__",node_labels[hosts_index[i]],sep="")
  }
  else {
    print(paste("missing ", curhost))
  }
  #}
}
row.names(virus_host__subtract) <- virus_host__subtract_label
dim(virus_host__subtract)

outfile <- "virus_host__subtract.tsv"
outfile_nodes <- "virus_host__subtract_labels.tsv"
print(outfile)
print(outfile_nodes)
write.table(virus_host__subtract, file=outfile, sep="\t")
write.table(virus_host__subtract_label, file=outfile, sep="\t")

full_index <- seq(1, length(node_labels), 1)
length(full_index)
length(hosts_index)
training_index <- hosts_index
sum(!(hosts_index %in% full_index))
negative_index <- full_index[!hosts_index %in% full_index]
negative_sample <- sample(1:length(negative_index), length(training_index))

sum(is.na(hosts))
sum(is.na(hosts_index))
length(unique(hosts[(hosts_index %in% full_index)]))
length(unique(hosts[!(hosts_index %in% full_index)]))
unique(hosts[!(hosts_index %in% full_index)])[1:10]


outfile <- "virus_host_NEGATIVE__subtract.tsv"
outfile_nodes <- "virus_host_NEGATIVE_subtract_labels.tsv"
print(outfile)
print(outfile_nodes)
write.table(new_virus_host__subtract, file=outfile, sep="\t")
write.table(new_virus_host__subtract_label, file=outfile, sep="\t")




random_new_viruses <- sample(1:length(vOTUs), 10)#runif(10, 0,  length(vOTUs))
match(random_new_viruses,hosts_index)

#random_new_viruses2 <- sample(1:length(vOTUs), 100000)#runif(10, 0,  length(vOTUs))
new_virus_host__subtract <- c()
new_virus_host__subtract_label <- c()
for(i in 1:length(random_new_viruses)){
  v_embed <- embeddings[random_new_viruses[i],]
    for(j in 1:length(hosts_index)){
      if(j %% 100) {
        print(j)
      }
      h_embed <- embeddings[hosts_index[j],]
      
      vh_embed <- v_embed - h_embed 
      new_virus_host__subtract <- rbind(new_virus_host__subtract, vh_embed)
      
      new_virus_host__subtract_label <- paste(node_labels[random_new_viruses[i]],"__",node_labels[hosts_index[j]],sep="")
    }
}
row.names(new_virus_host__subtract) <- new_virus_host__subtract_label

dim(new_virus_host__subtract)

outfile <- "virus_host_NEW__subtract.tsv"
outfile_nodes <- "virus_host_NEW_subtract_labels.tsv"
print(outfile)
print(outfile_nodes)
write.table(new_virus_host__subtract, file=outfile, sep="\t")
write.table(new_virus_host__subtract_label, file=outfile, sep="\t")







