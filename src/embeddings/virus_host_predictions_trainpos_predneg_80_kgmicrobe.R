rm(list=ls())
set.seed(12345)
setwd("/global/scratch/marcin/N2V/KE_KG/")

embeddings <- read.csv("/global/scratch/marcin/N2V/KE_KG/link_predict_kgmicrobe_shape_80/SkipGram_embedding_kgmicrobe_80.csv", sep="\t", header=TRUE, row.names=1)
head(embeddings)
dim(embeddings)

#node_data <- read.csv("../KE_KG/data/merged_last/IMGVR_merged_final_KGX_nodes.tsv", sep="\t",header=T)
node_data <- read.csv("/global/scratch/marcin/N2V/embiggen/notebooks/kg_microbe/20210315/merged-kg_nodes.tsv", sep="\t",header=T, quote="", stringsAsFactors = FALSE)
dim(node_data)
head(node_data) 

node_labels <- as.character(node_data$id)

#train_edges <- read.csv("/global/scratch/marcin/N2V/embiggen/notebooks/kg_microbe/20210119/merged_kg_edges_SHAPE_whead.tsv",sep="\t",header=T)
train_edges <- read.csv("/global/scratch/marcin/N2V/KE_KG/link_predict_kgmicrobe_shape_80/kgmicrobe_edges__positive80_Shape_whead.tsv",sep="\t",header=T)
dim(train_edges)
head(train_edges) 

#all_objects <-  read.csv("/global/scratch/marcin/N2V/embiggen/notebooks/kg_microbe/20210119/merged-kg_nodes_NCBITaxon_whead.tsv",sep="\t",header=T)
all_objects <-  read.csv("/global/scratch/marcin/N2V/KE_KG/link_predict_kgmicrobe_shape/merged-kg_nodes_NCBITaxon_whead.tsv",sep="\t",header=T)
dim(all_objects)
head(all_objects) 

subjects <- train_edges$object
length(subjects)
head(subjects)

objects <- train_edges$subject
objects_full <- all_objects$id
head(objects)
length(objects)
length(objects_full)

subjects_unique <- unique(subjects)

subjects_index <- match(subjects, node_labels)
objects_index <- match(objects, node_labels)
length(objects_index)
objects_full_index <- match(objects_full, node_labels)
head(objects_full)
length(objects_full_index)
length(subjects_index)
length(unique(objects))
sum(!is.na(objects_index))
sum(is.na(objects_index))
sum(!is.na(subjects_index))
sum(is.na(subjects_index))
objects[is.na(objects_index)][1:10]

length(unique(objects_full))
sum(!is.na(objects_full_index))
sum(is.na(objects_full_index))
objects[is.na(objects_full_index)][1:10]


train_edges__subtract <- data.frame()
train_edges__subtract_label <- c()

done <- FALSE#FALSE#TRUE
if(!done) {
  for(i in 1:length(subjects_index)){
    
    if(i %% 100 == 0) {
      print(paste("vh", i))
    }
    
    if(!is.na(objects_index[i])){
      curlabel <- paste(node_labels[subjects_index[i]],"__",node_labels[objects_index[i]],sep="")
      #print(curlabel)
      if(!(curlabel %in% train_edges__subtract_label)) {
        print(curlabel)
        #objindex <- which(hashost)
        subj_embed <- embeddings[subjects_index[i],]
        #for(j in 1:length(objects_index)){
        obj_embed <- embeddings[objects_index[i],]
        
        subj_obj_embed <- subj_embed - obj_embed 
        train_edges__subtract <- rbind(train_edges__subtract, subj_obj_embed)
        train_edges__subtract_label <- c(train_edges__subtract_label, curlabel)#,"__",i
      }
      #}
    }
    #else {
    #  print(paste("missing ", curobject))
    #}
    #}
  }
  row.names(train_edges__subtract) <- train_edges__subtract_label
  outfile <- "train_edges__subtract.tsv"
  outfile_nodes <- "train_edges__subtract_labels.tsv"
  print(outfile)
  print(outfile_nodes)
  write.csv(train_edges__subtract, file=outfile)
  write.table(train_edges__subtract_label, file=outfile_nodes, sep="\t")
} else {
  train_edges__subtract <- read.csv("train_edges__subtract.tsv", row.names=1, header=TRUE, sep=",")
  train_edges__subtract_label <- read.csv("train_edges__subtract_labels.tsv", sep="\t")[,1]
}

dim(train_edges__subtract)
length(train_edges__subtract_label)
head(train_edges__subtract)
head(train_edges__subtract_label)


###create negative samples
full_index <- seq(1, length(node_labels), 1)
length(full_index)
length(objects_full_index)


###all rows of training + duplicates
training_index_all <- match(train_edges$object, subjects_unique)
training_index_all_rev <- match(subjects_unique,train_edges$object)
length(training_index_all)
length(training_index_all_rev)

done <- FALSE
if(!done) {
  training_index <-c()
  negative_index <- c()
  for(i in 1:length(train_edges$subject))   {
    #print(train_edges$subject[i])
    
    if(!is.na(training_index_all[i]) && train_edges$object[i] != "" ) {
      training_index <-c(training_index, i)
    } else {
      negative_index <-c(negative_index, i)
    }
  }
  
  write.table(training_index, file="training_index.txt", row.names=F, col.name=F)
  write.table(negative_index, file="negative_index.txt", row.names=F, col.name=F)
} else {
  training_index <- read.table("training_index.txt", sep="\t")[,1]#, row.names=TRUE
  negative_index <- read.table("negative_index.txt", sep="\t")[,1]#, row.names=TRUE
}
length(training_index)
head(training_index)
length(negative_index)
head(negative_index)
###actual rows used for training


subjects_unique <- unique(subjects)
length(subjects_unique)
length(subjects[subjects_index])


sum(is.na(objects))
sum(is.na(objects_index))
length(unique(objects[(objects_index %in% full_index)]))
length(unique(objects[!(objects_index %in% full_index)]))
unique(objects[!(objects_index %in% full_index)])[1:10]


train_edges__subtract__NEG <- c()
train_edges__subtract_label__NEG <- c()
length(unique(objects))
length(unique(subjects[training_index]))

object_samples <- 5
###for all negative samples
for(i in 1:length(training_index)){
  if(i %% 100 == 0) {
    print(paste("v", i))
  }
  
  cursubject <- training_index[i]
  
  for(j in 1:object_samples){
    
    if(j %% 100 == 0) {
      print(paste("h", j))
    }
    
    curobject <- sample(1:length(objects_full), 1)#j
    
    curlabel <- paste(subjects[cursubject],"__",objects_full[curobject],sep="")
    #curlabel <- train_edges__subtract_label[1]
    #print(curlabel)
    #print(cursubject)
    #print(vOTUs[cursubject])
    #not in positive and not yet in negative
    if(!(curlabel %in% train_edges__subtract_label) && !(curlabel %in% train_edges__subtract_label__NEG) && !(curlabel %in% train_edges__subtract_label__NEG)) {
      
      objindex <- objects_full_index[curobject]
      subjindex <- subjects_index[cursubject]
      #print(objindex)
      #print(subjindex)
      #print(curobject)
      #print(cursubject)
      #print(node_labels[objindex])
      #print(node_labels[subjindex])
      
      subj_embed <- embeddings[subjindex,]
      #for(j in 1:length(objects_index)){
      obj_embed <- embeddings[objindex,]
      #print(dim(subj_embed))
      #print(dim(obj_embed))
      
      subj_obj_embed <- subj_embed - obj_embed 
      if(sum(is.na(subj_obj_embed)) >0 ) {
        print(paste("NA",curlabel, curobject, objindex, cursubject, subjindex))
        #if(sum(is.na(subj_embed)) >0 ) {
        #  print("VIRUS")
        #  print(subj_embed)
        #}
        #if(sum(is.na(obj_embed)) >0 ) {
        #  print("HOST")
        #}
        j <- j-1
      }
      else {
        #print("adding")
        train_edges__subtract__NEG <- rbind(train_edges__subtract__NEG, subj_obj_embed)
        train_edges__subtract_label__NEG <- c(train_edges__subtract_label__NEG, curlabel)
      }
    }
  }
}
row.names(train_edges__subtract__NEG) <- train_edges__subtract_label__NEG
dim(train_edges__subtract__NEG)



outfile <- "./train_edges_NEGATIVE__subtract.tsv"
outfile_nodes <- "train_edges_NEGATIVE__subtract_labels.tsv"
print(outfile)
print(outfile_nodes)
write.csv(train_edges__subtract__NEG, file=outfile)
write.table(train_edges__subtract_label__NEG, file=outfile_nodes, sep="\t")




random_new_viruses_sample <- sample(1:length(subjects), 10)
match(random_new_viruses_sample,objects_index)

new_train_edges__subtract <- c()
new_train_edges__subtract_label <- c()
for(i in 1:length(random_new_viruses_sample)){
  subj_embed <- embeddings[subjects_index[random_new_viruses_sample[i]],]
  for(j in 1:length(objects_index)){
    
    curlabel <- paste(node_labels[subjects_index[random_new_viruses_sample[i]]],"__",node_labels[objects_index[j]],sep="")
    
    if(!(curlabel %in% new_train_edges__subtract_label)) {
      if(j %% 100) {
        print(j)
      }
      obj_embed <- embeddings[objects_index[j],]
      
      subj_obj_embed <- subj_embed - obj_embed 
      new_train_edges__subtract <- rbind(new_train_edges__subtract, subj_obj_embed)
      new_train_edges__subtract_label <- c(new_train_edges__subtract_label, curlabel)
    }
  }
}
row.names(new_train_edges__subtract) <- new_train_edges__subtract_label

dim(new_train_edges__subtract)

write.table(random_new_viruses_sample, file="train_edges__random10_sample.tsv", sep="\t")


outfile <- "train_edges_NEW__subtract.tsv"
outfile_nodes <- "train_edges_NEW_subtract_labels.tsv"
print(outfile)
print(outfile_nodes)
write.csv(new_train_edges__subtract, file=outfile)
write.table(new_train_edges__subtract_label, file=outfile_nodes, sep="\t")







