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
host_raw <- unique(virus_host$Host_taxonomy_prediction[hlens>1])
host_raw_full <- virus_host$Host_taxonomy_prediction[hlens>1]

hosts <- paste("NCBItaxon:",tolower(unique(virus_host$Host_taxonomy_prediction[hlens>1])),sep="")
hosts_full <- paste("NCBItaxon:",tolower(virus_host$Host_taxonomy_prediction[hlens>1]),sep="")
hosts_full_all <- paste("NCBItaxon:",tolower(virus_host$Host_taxonomy_prediction),sep="")#hosts <- gsub(" ","_",hosts)
length(hosts)
length(hosts_full)
length(hosts_full_all)
class(node_labels[1])

grep("vOTU:votu_219688", node_labels)
#vOTUs_index <- vOTUs %in% node_labels
#hosts_index <- hosts %in% node_labels
vOTUs_index <- match(vOTUs, node_labels)
hosts_index <- match(hosts, node_labels)
length(hosts_index)
hosts_full_index <- match(hosts_full, node_labels)
hosts_full_all_index <- match(hosts_full_all, node_labels)
length(hosts_full_index)
length(hosts_full_all_index)
length(vOTUs_index)
length(unique(hosts))
sum(!is.na(hosts_index))
sum(is.na(hosts_index))
hosts[is.na(hosts_index)][1:10]

length(unique(hosts_full))
sum(!is.na(hosts_full_index))
sum(is.na(hosts_full_index))
hosts[is.na(hosts_full_index)][1:10]

host_curie <- paste("NCBItaxon:",tolower(virus_host$Host_taxonomy_prediction),sep="")


virus_host__subtract <- data.frame()
virus_host__subtract_label <- c()

done <- TRUE
if(!done) {
  for(i in 1:length(vOTUs_index)){
    
    #curhost <- host_curie[i]
    #print(curhost)
    #hashost <- curhost %in% hosts
    
    #print(hashost)
    #if(hashost) {
    if(i %% 100 == 0) {
      print(paste("vh", i))
    }
    
    if(!is.na(hosts_full_all_index[i])){
      curlabel <- paste(node_labels[vOTUs_index[i]],"__",node_labels[hosts_full_all_index[i]],sep="")
      print(curlabel)
      if(!(curlabel %in% virus_host__subtract_label)) {
        print(curlabel)
        #hindex <- which(hashost)
        v_embed <- embeddings[vOTUs_index[i],]
        #for(j in 1:length(hosts_index)){
        h_embed <- embeddings[hosts_full_all_index[i],]
        
        vh_embed <- v_embed - h_embed 
        virus_host__subtract <- rbind(virus_host__subtract, vh_embed)
        virus_host__subtract_label <- c(virus_host__subtract_label, curlabel)#,"__",i
      }
    #}
    }
    #else {
    #  print(paste("missing ", curhost))
    #}
    #}
  }
  row.names(virus_host__subtract) <- virus_host__subtract_label
  outfile <- "virus_host__subtract.tsv"
  outfile_nodes <- "virus_host__subtract_labels.tsv"
  print(outfile)
  print(outfile_nodes)
  write.csv(virus_host__subtract, file=outfile)
  write.table(virus_host__subtract_label, file=outfile_nodes, sep="\t")
} else {
  virus_host__subtract <- read.csv("virus_host__subtract.tsv", row.names=1, header=TRUE, sep=",")
  virus_host__subtract_label <- read.csv("virus_host__subtract_labels.tsv", sep="\t")
}

dim(virus_host__subtract)
dim(virus_host__subtract_label)
head(virus_host__subtract)
head(virus_host__subtract_label)


###create negative samples
full_index <- seq(1, length(node_labels), 1)
length(full_index)
length(hosts_full_index)

###pick the virus-host pairs, but only one if multiple
###however, mask all virus-host pairs including duplicates
testlen_unique_virus_host <- dim(virus_host__subtract)[1]



###all rows of training + duplicates
training_index_all <- match(virus_host$Host_taxonomy_prediction, host_raw)
training_index_all_rev <- match(host_raw,virus_host$Host_taxonomy_prediction)
length(training_index_all)
length(training_index_all_rev)

done <- TRUE
if(!done) {
  training_index <-c()
  negative_index <- c()
  for(i in 1:length(virus_host$Host_taxonomy_prediction))   {
    print(virus_host$Host_taxonomy_prediction[i])
    
    if(!is.na(training_index_all[i]) && virus_host$Host_taxonomy_prediction[i] != "" ) {
      training_index <-c(training_index, i)
    } else {
      negative_index <-c(negative_index, i)
    }
  }
  
  write.table(training_index, file="training_index.txt")
  write.table(negative_index, file="negative_index.txt")
} else {
  training_index <- read.table("training_index.txt", sep="\t")#, row.names=TRUE
  negative_index <- read.table("negative_index.txt", sep="\t")#, row.names=TRUE
}
dim(training_index)
head(training_index[,1])
dim(negative_index)
length(negative_index)
###actual rows used for training


vOTUs_unique <- unique(vOTUs)
length(hosts)
length(vOTUs[hosts_index])

###
###
#print("ERROR hosts_full_index indexes against nodes, but need virus-host index !!!")
###
#virus_host_combos <- paste(vOTUs[hosts_full_index],"__",hosts_full,sep="")
#length(virus_host_combos)


negative_sample <- sample(1:length(negative_index[,1]), length(virus_host__subtract_label[,1]))
head(negative_sample)
length(negative_sample)

sum(!is.na(match(negative_index[negative_sample,1], training_index[,1])))

#sum(!is.na(match(negative_index[negative_sample], hosts_full_index)))
#hosts_full_index[match(negative_index[negative_sample], hosts_full_index)]
#node_labels[hosts_full_index]

write.table(negative_sample, file="virus_host__negative_sample.tsv", sep="\t")

sum(is.na(hosts))
sum(is.na(hosts_index))
length(unique(hosts[(hosts_index %in% full_index)]))
length(unique(hosts[!(hosts_index %in% full_index)]))
unique(hosts[!(hosts_index %in% full_index)])[1:10]


virus_host__subtract__NEG <- c()
virus_host__subtract_label__NEG <- c()

###for all negative samples
for(i in 1:length(negative_sample)){
  if(i %% 100 == 0) {
    print(paste("v", i))
  }
  
  #random virus
  curvir <- sample(1:length(vOTUs), 1)
  #random host
  curhost <- sample(1:length(hosts), 1)
  
  curlabel <- paste(vOTUs[curvir],"__",hosts[curhost],sep="")
  #curlabel <- virus_host__subtract_label[1]
  #print(curlabel)
  if(!(curlabel %in% virus_host__subtract_label) && !(curlabel %in% virus_host__subtract_label__NEG)) {
    
    #hindex <- match(node_labels, hosts[curhost])
    hindex <- hosts_index[curhost]
    #print(hindex)
    #print(node_labels[hindex])
    
    v_embed <- embeddings[curvir,]
    #for(j in 1:length(hosts_index)){
    h_embed <- embeddings[hindex,]
    
    vh_embed <- v_embed - h_embed 
    virus_host__subtract__NEG <- rbind(virus_host__subtract__NEG, vh_embed)
    virus_host__subtract_label__NEG <- c(virus_host__subtract_label__NEG, curlabel)
  }
  else {
    i <- i-1
    print("BACK")
    print(curlabel)
  }
}
row.names(virus_host__subtract__NEG) <- virus_host__subtract_label__NEG
dim(virus_host__subtract__NEG)



outfile <- "virus_host_NEGATIVE__subtract.tsv"
outfile_nodes <- "virus_host_NEGATIVE_subtract_labels.tsv"
print(outfile)
print(outfile_nodes)
write.csv(virus_host__subtract__NEG, file=outfile)
write.table(virus_host__subtract_label__NEG, file=outfile_nodes, sep="\t")




random_new_viruses_sample <- sample(1:length(vOTUs), 10)#runif(10, 0,  length(vOTUs))
match(random_new_viruses_sample,hosts_index)

#random_new_viruses2 <- sample(1:length(vOTUs), 100000)#runif(10, 0,  length(vOTUs))
new_virus_host__subtract <- c()
new_virus_host__subtract_label <- c()
for(i in 1:length(random_new_viruses_sample)){
  v_embed <- embeddings[random_new_viruses_sample[i],]
    for(j in 1:length(hosts_index)){
      if(j %% 100) {
        print(j)
      }
      h_embed <- embeddings[hosts_index[j],]
      
      vh_embed <- v_embed - h_embed 
      new_virus_host__subtract <- rbind(new_virus_host__subtract, vh_embed)
      new_virus_host__subtract_label <- c(paste(node_labels[random_new_viruses_sample[i]],"__",node_labels[hosts_index[j]],sep=""))
    }
}
row.names(new_virus_host__subtract) <- new_virus_host__subtract_label

dim(new_virus_host__subtract)

write.table(random_new_viruses_sample, file="virus_host__random10_sample.tsv", sep="\t")


outfile <- "virus_host_NEW__subtract.tsv"
outfile_nodes <- "virus_host_NEW_subtract_labels.tsv"
print(outfile)
print(outfile_nodes)
write.csv(new_virus_host__subtract, file=outfile)
write.table(new_virus_host__subtract_label, file=outfile_nodes, sep="\t")







