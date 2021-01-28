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
hosts <- paste("NCBItaxon:",tolower(virus_host$Host_taxonomy_prediction[hlens>1]),sep="")
length(hosts)
class(node_labels[1])

grep("vOTU:votu_219688", node_labels)
#vOTUs_index <- vOTUs %in% node_labels
#hosts_index <- hosts %in% node_labels
vOTUs_index <- match(vOTUs, node_labels)
hosts_index <- match(hosts, node_labels)

virus_host__subtract <- c()
virus_host__subtract_label <- c()
for(i in 1:length(vOTUs_index)){
  if(i %% 100) {
    print(".")
  }
  v_embed <- embeddings[vOTUs_index[i],]
  #for(j in 1:length(hosts_index)){
  h_embed <- embeddings[hosts_index[i],]
  
  vh_embed <- v_embed - h_embed 
  virus_host__subtract <- rbind(virus_host__subtract, vh_embed)
  
  virus_host__subtract_label <- paste(node_labels[vOTUs_index[i]],"__",node_labels[hosts_index[i]],sep="")
  #}
}
row.names(virus_host__subtract) <- virus_host__subtract_label
dim(virus_host__subtract)

outfile <- "virus_host__subtract.tsv"
outfile_nodes <- "virus_host__subtract_labels.tsv"

write.table(virus_host__subtract, file=outfile, sep="\t")
write.table(virus_host__subtract_label, file=outfile, sep="\t")


random_new_viruses <- sample(1:length(vOTUs), 10)#runif(10, 0,  length(vOTUs))
match(random_new_viruses,hosts_index)

#random_new_viruses2 <- sample(1:length(vOTUs), 100000)#runif(10, 0,  length(vOTUs))
new_virus_host__subtract <- c()
new_virus_host__subtract_label <- c()
for(i in 1:length(random_new_viruses)){
  v_embed <- embeddings[random_new_viruses[i],]
    for(j in 1:length(hosts_index)){
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

write.table(new_virus_host__subtract, file=outfile, sep="\t")
write.table(new_virus_host__subtract_label, file=outfile, sep="\t")





