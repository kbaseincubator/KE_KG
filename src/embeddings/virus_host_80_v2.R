rm(list = ls())
set.seed(12345)

setwd("/global/scratch/marcin/N2V/KE_KG")

embeddings <-
  read.csv(
    "/global/scratch/marcin/N2V/KE_KG/data/SkipGram_embedding_merged_imgvr_mg_good_train80.tsv",
    sep = "\t",
    header = TRUE,
    row.names = 1
  )
head(embeddings)
dim(embeddings)
#node_data <- read.csv("../KE_KG/data/merged_last/IMGVR_merged_final_KGX_nodes.tsv", sep="\t",header=T)
node_data <-
  read.csv(
    #"/global/scratch/marcin/N2V/KE_KG/link_predict_mg_imgvr_OPT_v5_80/IMGVR_merged_kg_nodes__positive80.tsv",
    "/global/scratch/marcin/N2V/KE_KG/data/merged_imgvr_mg_nodes_good.tsv",
    sep = "\t",
    header = T
  )
dim(node_data)
head(node_data)
node_labels <- as.character(node_data$id)


edge_data_test <-
  read.csv(
    "/global/scratch/marcin/N2V/KE_KG/data/merged_imgvr_mg_edges_good__test20.tsv",
    sep = "\t",
    header = T#, row.names=1
  )
dim(edge_data_test)
head(edge_data_test)


virus_host <-
  read.csv(
    "/global/scratch/marcin/N2V/KE_KG/data/IMGVR_all_Sequence_information_InIMG-Yes_Linked-to_TaxonOIDs_v2_Completeness-50-100_nocol20_v1.tsv",
    #"./IMGVR_all_Sequence_information_InIMG-Yes_Linked-to_TaxonOIDs_v2_Completeness-50-100_nocol20_v1.tsv",
    sep = "\t",
    header = T
  )
dim(virus_host)
head(virus_host)


head(virus_host$vOTU)

hindex_not <- which(virus_host$Host_taxonomy_prediction == "")
virus_host_combos <- paste("vOTU:",tolower(virus_host$vOTU[-hindex_not]),"__", "NCBItaxon:",gsub( " ", "_", tolower(virus_host$Host_taxonomy_prediction[-hindex_not])), sep = "")
head(virus_host_combos)
write.table(virus_host_combos, "virus_host_combos.txt",sep="\t")


vOTUs <- paste("vOTU:", tolower(virus_host$vOTU), sep = "")
length(vOTUs)
class(virus_host$Host_taxonomy_prediction[1])
length(virus_host$Host_taxonomy_prediction[1])
hlens <-
  nchar(as.character(virus_host$Host_taxonomy_prediction))#unlist(lapply(virus_host$Host_taxonomy_prediction, length))#lengths(virus_host$Host_taxonomy_prediction)
sum(hlens > 1)
#virus_host$Host_taxonomy_prediction[hlens>1]

virus_host$Host_taxonomy_prediction <-
  gsub(" ", "_", virus_host$Host_taxonomy_prediction)
host_raw <- unique(virus_host$Host_taxonomy_prediction[hlens > 1])
host_raw_full <- virus_host$Host_taxonomy_prediction[hlens > 1]

hosts <-
  paste("NCBItaxon:", tolower(unique(virus_host$Host_taxonomy_prediction[hlens >
                                                                           1])), sep = "")
hosts_full <-
  paste("NCBItaxon:",
        tolower(virus_host$Host_taxonomy_prediction[hlens > 1]),
        sep = "")
hosts_full_all <-
  paste("NCBItaxon:",
        tolower(virus_host$Host_taxonomy_prediction),
        sep = "")#hosts <- gsub(" ","_",hosts)
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

host_curie <-
  paste("NCBItaxon:",
        tolower(virus_host$Host_taxonomy_prediction),
        sep = "")


edge_data_test_labels <-
  row.names(edge_data_test)#paste(edge_data_test[, 'subject'],"__",edge_data_test[, 'object'], sep="")



virus_host__subtract__TEST <- data.frame()
virus_host__subtract_label__TEST <- c()

#create new subtractions based on test sample subtraction from 100% graph emebeddings
done <- TRUE#FALSE#TRUE
if (!done) {
  ###for all test samples
  for (i in 1:dim(edge_data_test)[1]) {
    if (i %% 100 == 0) {
      print(paste("t", i))
    }
    curlabel <- paste(edge_data_test$object[i],"__",edge_data_test$subject[i], sep="")#row.names(edge_data_test)[i]
    
    #print(curlabel %in% virus_host__subtract_label__TEST)
    #not in positive and not in negative and not yet in test
    if (!(curlabel %in% virus_host__subtract_label__TEST)) {
      #curlabels <- strsplit(curlabel, "__")
      
      curvir <- edge_data_test$object[i]#curlabels[[1]][1]#strsplit(curlabels[0], "\t")[2]
      curvir_tab <- gregexpr(pattern ='\t',curvir)
      if(curvir_tab[[1]][1] > -1) {
        curvir <- substr(curvir, curvir_tab[[1]][1]+1, nchar(curvir))
        print("trimmed curvir by \t")
      }
      curhost <- edge_data_test$subject[i]#curlabels[[1]][2]
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
        virus_host__subtract__TEST <-
          rbind(virus_host__subtract__TEST, vh_embed)
        virus_host__subtract_label__TEST <-
          c(virus_host__subtract_label__TEST, curlabel)
      }
    }
  }
} else {
  virus_host__subtract__TEST <-
    read.csv(
      "virus_host_TEST__subtract.tsv",
      row.names = 1,
      header = TRUE,
      sep = ","
    )
  virus_host__subtract_label__TEST <-
    read.csv("virus_host_TEST__subtract_labels.tsv", sep = "\t")[, 1]
}
row.names(virus_host__subtract__TEST) <-
  virus_host__subtract_label__TEST
dim(virus_host__subtract__TEST)


outfile <- "./virus_host_TEST__subtract.tsv"
outfile_nodes <- "virus_host_TEST__subtract_labels.tsv"
print(outfile)
print(outfile_nodes)
write.csv(virus_host__subtract__TEST, file = outfile)
write.table(virus_host__subtract_label__TEST,
            file = outfile_nodes,
            sep = "\t")



virus_host__subtract <- data.frame()
virus_host__subtract_label <- c()

done <- TRUE#FALSE#TRUE
if (!done) {
  for (i in 1:length(vOTUs_index)) {
    #curhost <- host_curie[i]
    #print(curhost)
    #hashost <- curhost %in% hosts
    
    #print(hashost)
    #if(hashost) {
    if (i %% 100 == 0) {
      print(paste("vh", i))
    }
    
    if (!is.na(hosts_full_all_index[i])) {
      curlabel <-
        paste(node_labels[vOTUs_index[i]], "__", node_labels[hosts_full_all_index[i]], sep =
                "")
      #print(curlabel)
      if (!(curlabel %in% virus_host__subtract_label) &&
          !(curlabel %in% virus_host__subtract_label__TEST)) {
        #print(curlabel)
        #hindex <- which(hashost)
        v_embed <- embeddings[vOTUs_index[i],]
        #for(j in 1:length(hosts_index)){
        h_embed <- embeddings[hosts_full_all_index[i],]
        
        vh_embed <- v_embed - h_embed
        virus_host__subtract <-
          rbind(virus_host__subtract, vh_embed)
        virus_host__subtract_label <-
          c(virus_host__subtract_label, curlabel)#,"__",i
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
  write.csv(virus_host__subtract, file = outfile)
  write.table(virus_host__subtract_label,
              file = outfile_nodes,
              sep = "\t")
} else {
  virus_host__subtract <-
    read.csv(
      "virus_host__subtract.tsv",
      row.names = 1,
      header = TRUE,
      sep = ","
    )
  virus_host__subtract_label <-
    read.csv("virus_host__subtract_labels.tsv", sep = "\t")[, 1]
}

dim(virus_host__subtract)
length(virus_host__subtract_label)
head(virus_host__subtract)
head(virus_host__subtract_label)

outfile <- "./virus_host__subtract.tsv"
outfile_nodes <- "virus_host__subtract_labels.tsv"
print(outfile)
print(outfile_nodes)
write.csv(virus_host__subtract, file = outfile)
write.table(virus_host__subtract_label,
            file = outfile_nodes,
            sep = "\t")


###create negative samples
full_index <- seq(1, length(node_labels), 1)
length(full_index)
length(hosts_full_index)

###pick the virus-host pairs, but only one if multiple
###however, mask all virus-host pairs including duplicates
testlen_unique_virus_host <- dim(virus_host__subtract)[1]



###all rows of training + duplicates
training_index_all <-
  match(virus_host$Host_taxonomy_prediction, host_raw)
training_index_all_rev <-
  match(host_raw, virus_host$Host_taxonomy_prediction)
length(training_index_all)
length(training_index_all_rev)

done <- TRUE#FALSE#TRUE
if (!done) {
  training_index <- c()
  negative_index <- c()
  for (i in 1:length(virus_host$Host_taxonomy_prediction))   {
    #print(virus_host$Host_taxonomy_prediction[i])
    
    if (!is.na(training_index_all[i]) &&
        virus_host$Host_taxonomy_prediction[i] != "") {
      training_index <- c(training_index, i)
    } else {
      negative_index <- c(negative_index, i)
    }
  }
  
  write.table(
    training_index,
    file = "training_index.txt",
    row.names = F,
    col.name = F
  )
  write.table(
    negative_index,
    file = "negative_index.txt",
    row.names = F,
    col.name = F
  )
} else {
  training_index <-
    read.table("training_index.txt", sep = "\t")[, 1]#, row.names=TRUE
  negative_index <-
    read.table("negative_index.txt", sep = "\t")[, 1]#, row.names=TRUE
}
dim(training_index)
head(training_index)
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



sum(is.na(hosts))
sum(is.na(hosts_index))
length(unique(hosts[(hosts_index %in% full_index)]))
length(unique(hosts[!(hosts_index %in% full_index)]))
unique(hosts[!(hosts_index %in% full_index)])[1:10]


virus_host__subtract__NEG <- c()
virus_host__subtract_label__NEG <- c()
length(unique(hosts))
length(unique(vOTUs[training_index]))

host_samples <- 1

done <- TRUE
if(!done) {
###for all negative samples
for (i in 1:length(training_index)) {
  if (i %% 100 == 0) {
    print(paste("v", i))
  }
  
  #random virus
  curvir <- training_index[i]#sample(1:length(vOTUs), 1)
  #print(curvir)
  #random host
  for (j in 1:host_samples) {
    #length(hosts)){
    
    if (j %% 100 == 0) {
      print(paste("h", j))
    }
    
    curhost <- sample(1:length(hosts), 1)#j
    
    curlabel <- paste(vOTUs[curvir], "__", hosts[curhost], sep = "")
    #curlabel <- virus_host__subtract_label[1]
    #print(curlabel)
    #print(curvir)
    #print(vOTUs[curvir])
    #not in positive and not yet in negative
    if (!(curlabel %in% virus_host__subtract_label) &&
        !(curlabel %in% virus_host__subtract_label__TEST) &&
        !(curlabel %in% virus_host__subtract_label__NEG)) {
      #hindex <- match(node_labels, hosts[curhost])
      hindex <- hosts_index[curhost]
      vindex <- vOTUs_index[curvir]
      #print(hindex)
      #print(node_labels[hindex])
      
      v_embed <- embeddings[vindex,]
      #for(j in 1:length(hosts_index)){
      h_embed <- embeddings[hindex,]
      
      vh_embed <- v_embed - h_embed
      if (sum(is.na(vh_embed)) > 0) {
        print(paste("NA", curlabel, curhost, hindex, curvir, vindex))
        #if(sum(is.na(v_embed)) >0 ) {
        #  print("VIRUS")
        #  print(v_embed)
        #}
        #if(sum(is.na(h_embed)) >0 ) {
        #  print("HOST")
        #}
        j <- j - 1
      }
      else {
        #print("adding")
        virus_host__subtract__NEG <-
          rbind(virus_host__subtract__NEG, vh_embed)
        virus_host__subtract_label__NEG <-
          c(virus_host__subtract_label__NEG, curlabel)
      }
    }
  }
}
  row.names(virus_host__subtract__NEG) <-
    virus_host__subtract_label__NEG
  dim(virus_host__subtract__NEG)
  
  outfile <- "./virus_host_NEGATIVE__subtract.tsv"
  outfile_nodes <- "virus_host_NEGATIVE__subtract_labels.tsv"
  print(outfile)
  print(outfile_nodes)
  write.csv(virus_host__subtract__NEG, file = outfile)
  write.table(virus_host__subtract_label__NEG,
              file = outfile_nodes,
              sep = "\t")
}




random_new_viruses_sample <-
  sample(1:length(vOTUs), 3)#runif(10, 0,  length(vOTUs))
#match(random_new_viruses_sample, hosts_index)

random_new_viruses_sample <- c()
max_new_viruses <- 5
for( i in 1:5) {
  newvir <- sample(1:length(vOTUs), 1)
  
    search1 <- grep(vOTUs[newvir], virus_host__subtract_label)
    search2 <- grep(vOTUs[newvir], virus_host__subtract_label__TEST)
    if(length(search1) == 0 && length(search2) == 0) {
      random_new_viruses_sample <- c(random_new_viruses_sample, newvir)
  }
}


#random_new_viruses2 <- sample(1:length(vOTUs), 100000)#runif(10, 0,  length(vOTUs))
new_virus_host__subtract <- c()
new_virus_host__subtract_label <- c()
for (i in 1:length(random_new_viruses_sample)) {
  v_embed <- embeddings[vOTUs_index[random_new_viruses_sample[i]],]
  #if (i %% 100 == 0) {
  print(paste("i ",i))
  #}
  for (j in 1:length(hosts_index)) {
    curlabel <-
      paste(node_labels[vOTUs_index[random_new_viruses_sample[i]]], "__", node_labels[hosts_index[j]], sep =
              "")
    #if (
      #!(curlabel %in% new_virus_host__subtract_label) &&
        #!(curlabel %in% virus_host__subtract_label) &&
        #!(curlabel %in% virus_host__subtract__NEG) &&
        #!(curlabel %in% virus_host__subtract_label__TEST)) {
      if (j %% 100 == 0) {
        print(paste("j ",j))
      }
      h_embed <- embeddings[hosts_index[j],]
      
      vh_embed <- v_embed - h_embed
      new_virus_host__subtract <-
        rbind(new_virus_host__subtract, vh_embed)
      new_virus_host__subtract_label <-
        c(new_virus_host__subtract_label, curlabel)
    #}
  }
}
row.names(new_virus_host__subtract) <-
  new_virus_host__subtract_label

dim(new_virus_host__subtract)

write.table(random_new_viruses_sample, file = "virus_host__random10_sample.tsv", sep ="\t")


outfile <- "virus_host_NEW__subtract.tsv"
outfile_nodes <- "virus_host_NEW_subtract_labels.tsv"
print(outfile)
print(outfile_nodes)
write.csv(new_virus_host__subtract, file = outfile)
write.table(new_virus_host__subtract_label,
            file = outfile_nodes,
            sep = "\t")

####
####
####
virus_host__subtract_label__TEST <-
  read.csv("./link_predict_mg_imgvr_OPT_v5_80/virus_host_TEST__subtract_labels.tsv", sep = "\t")[, 1]

match_ref_TEST <- match(virus_host__subtract_label__TEST, virus_host_combos)
sum(is.na(match_ref_TEST))
sum(!is.na(match_ref_TEST))
match_ref_TEST_pos_neg <- rep(1, length(virus_host__subtract_label__TEST) )
match_ref_TEST_pos_neg[is.na(match_ref_TEST)] <- 0
write.table(match_ref_TEST_pos_neg,
            file = "virus_host_TEST__subtract_pos_neg.tsv",
            sep = "\t")

#virus_host__subtract
virus_host__subtract_label <-
  read.csv("./link_predict_mg_imgvr_OPT_v5_80/virus_host__subtract_labels.tsv", sep = "\t")[, 1]

match_ref <- match(virus_host__subtract_label, virus_host_combos)
sum(is.na(match_ref))
sum(!is.na(match_ref))


#virus_host__subtract
virus_host__subtract_label__NEG <-
  read.csv("./link_predict_mg_imgvr_OPT_v5_80/virus_host_NEGATIVE__subtract_labels.tsv", sep = "\t")[, 1]

match_neg <- match(virus_host__subtract_label__NEG, virus_host_combos)
sum(is.na(match_neg))
sum(!is.na(match_neg))


