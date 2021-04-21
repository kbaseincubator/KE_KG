rm(list=ls())
set.seed(12345)


embeddings <- read.csv("/global/scratch/marcin/N2V/KE_KG/link_predict_kgmicrobe_shape_80/SkipGram_embedding_kgmicrobe_train80shape.tsv", sep="\t", header=TRUE, row.names=1)
head(embeddings)
dim(embeddings)
#node_data <- read.csv("../KE_KG/data/merged_last/IMGVR_merged_final_KGX_nodes.tsv", sep="\t",header=T)
node_data <- read.csv("/global/scratch/marcin/N2V/KE_KG/link_predict_kgmicrobe_shape_80/merged-kg_nodes.tsv", sep="\t",header=T, quote="", stringsAsFactors = FALSE)
dim(node_data)
head(node_data) 
node_labels <- as.character(node_data$id)

train_edges <- read.csv("/global/scratch/marcin/N2V/KE_KG/link_predict_kgmicrobe_shape_80/merged-kg_edges__shape__train80.tsv",sep="\t",header=T)
dim(train_edges)
head(train_edges) 

test_edges <- read.csv("/global/scratch/marcin/N2V/KE_KG/link_predict_kgmicrobe_shape_80/merged-kg_edges__shape__test20.tsv",sep="\t",header=T)
dim(test_edges)
head(test_edges) 

all_objects <-  read.csv("/global/scratch/marcin/N2V/KE_KG/link_predict_kgmicrobe_shape_80/merged-kg_nodes_NCBITaxon_whead.tsv",sep="\t",header=T)
dim(all_objects)
head(all_objects) 



#train_edges_labels <- row.names(train_edges)
#test_edges_split <- strsplit(train_edges_labels, "__")
#subjsplit_raw <- unlist(test_edges_split)[2*(1:length(test_edges_split))-1]
#head(subjsplit_raw)
#subjects <- unlist(strsplit(as.character(subjsplit_raw), "\t", fixed=TRUE))[2*(1:length(test_edges_split))]
#head(subjects)
#objects  <- unlist(test_edges_split)[2*(1:length(test_edges_split))  ]
#head(objects)


subjects <- train_edges$object
head(subjects)
objects  <- train_edges$subject
head(objects)

length(subjects)
head(subjects)
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




taxa_trait__subtract__TEST <- data.frame()
taxa_trait__subtract_label__TEST <- c()

#create new subtractions based on test sample subtraction from 100% graph emebeddings
done <- FALSE#FALSE#TRUE
if (!done) {
  ###for all test samples
  for (i in 1:dim(test_edges)[1]) {
    if (i %% 100 == 0) {
      print(paste("t", i))
    }
    curlabel <- paste(test_edges$object[i],"__",test_edges$subject[i], sep="")#row.names(edge_data_test)[i]
    
    #print(curlabel %in% taxa_trait__subtract_label__TEST)
    #not in positive and not in negative and not yet in test
    if (!(curlabel %in% taxa_trait__subtract_label__TEST)) {
      #curlabels <- strsplit(curlabel, "__")
      
      curvir <- test_edges$object[i]#curlabels[[1]][1]#strsplit(curlabels[0], "\t")[2]
      curvir_tab <- gregexpr(pattern ='\t',curvir)
      if(curvir_tab[[1]][1] > -1) {
        curvir <- substr(curvir, curvir_tab[[1]][1]+1, nchar(curvir))
        print("trimmed curvir by \t")
      }
      curhost <- test_edges$subject[i]#curlabels[[1]][2]
      #print(paste(curvir, curhost))
      
      vindex <- match(curvir, node_labels)
      hindex <- match(curhost, node_labels)
      
      #print(hindex)
      #print(node_labels[hindex])
      
      v_embed <- embeddings[vindex,]
      #for(j in 1:length(hosts_index)){
      h_embed <- embeddings[hindex,]
      
      vh_embed <- v_embed - h_embed
      if (sum(is.na(vh_embed)) > 0) {
        print(curlabel)
        print(paste(vindex, hindex))
        print(paste("NA", curlabel, curhost, hindex, curvir, vindex))
      }
      else {
        #print("adding")
        taxa_trait__subtract__TEST <-
          rbind(taxa_trait__subtract__TEST, vh_embed)
        taxa_trait__subtract_label__TEST <-
          c(taxa_trait__subtract_label__TEST, curlabel)
      }
    }
  }
} else {
  taxa_trait__subtract__TEST <-
    read.csv(
      "taxa_trait_TEST__subtract.tsv",
      row.names = 1,
      header = TRUE,
      sep = ","
    )
  taxa_trait__subtract_label__TEST <-
    read.csv("taxa_trait_TEST__subtract_labels.tsv", sep = "\t")[, 1]
}
row.names(taxa_trait__subtract__TEST) <-
  taxa_trait__subtract_label__TEST
dim(taxa_trait__subtract__TEST)


outfile <- "./taxa_trait_TEST__subtract.tsv"
outfile_nodes <- "taxa_trait_TEST__subtract_labels.tsv"
print(outfile)
print(outfile_nodes)
write.csv(taxa_trait__subtract__TEST, file = outfile)
write.table(taxa_trait__subtract_label__TEST,
            file = outfile_nodes,
            sep = "\t")




train_edges__subtract <- data.frame()
train_edges__subtract_label <- c()

done <- FALSE#FALSE#TRUE
if(!done) {
  for(i in 1:length(subjects_index)){
    
    if(i %% 100 == 0) {
      print(paste("vh", i))
    }
    
    if(!is.na(objects_full_index[i])){
      curlabel <- paste(node_labels[subjects_index[i]],"__",node_labels[objects_full_index[i]],sep="")
      #print(curlabel)
      if(length(curlabel) > 0 && !(curlabel %in% train_edges__subtract_label) && !(curlabel %in% taxa_trait__subtract_label__TEST)) {
        #print(curlabel)
        #objindex <- which(hashost)
        subj_embed <- embeddings[subjects_index[i],]
        #for(j in 1:length(objects_index)){
        obj_embed <- embeddings[objects_full_index[i],]
        
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
  outfile <- "taxa_trait__subtract.tsv"
  outfile_nodes <- "taxa_trait__subtract_labels.tsv"
  print(outfile)
  print(outfile_nodes)
  write.csv(train_edges__subtract, file=outfile)
  write.table(train_edges__subtract_label, file=outfile_nodes, sep="\t")
} else {
  train_edges__subtract <- read.csv("taxa_trait__subtract.tsv", row.names=1, header=TRUE, sep=",")
  train_edges__subtract_label <- read.csv("taxa_trait__subtract_labels.tsv", sep="\t")[,1]
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
    
    curobject <- sample(1:length(objects), 1)#j
    
    curlabel <- paste(subjects[cursubject],"__",objects[curobject],sep="")
    #curlabel <- train_edges__subtract_label[1]
    #print(curlabel)
    #print(cursubject)
    #print(vOTUs[cursubject])
    #not in positive and not yet in negative
    if(!(curlabel %in% train_edges__subtract_label) && !(curlabel %in% taxa_trait__subtract_label__TEST) && !(curlabel %in% train_edges__subtract_label__NEG) ) {
      
      objindex <- objects_index[curobject]
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



outfile <- "./taxa_trait_NEGATIVE__subtract.tsv"
outfile_nodes <- "taxa_trait_NEGATIVE__subtract_labels.tsv"
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
    
    if(!(curlabel %in% new_train_edges__subtract_label) && !(curlabel %in% train_edges__subtract_label) && !(curlabel %in% taxa_trait__subtract_label__TEST) ) {
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

write.table(random_new_viruses_sample, file="taxa_trait__random10_sample_80.tsv", sep="\t")


outfile <- "taxa_trait_NEW__subtract_80.tsv"
outfile_nodes <- "taxa_trait_NEW_subtract_labels_80.tsv"
print(outfile)
print(outfile_nodes)
write.csv(new_train_edges__subtract, file=outfile)
write.table(new_train_edges__subtract_label, file=outfile_nodes, sep="\t")







