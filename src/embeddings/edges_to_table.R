rm(list=ls())
setwd("~/Documents/KBase/KE/KE_KG/")
#library("reshape2")
#library("data.table")

edge_data <- read.csv("../IMGVR/IMGVR_merged_kg_edges.tsv", sep="\t",header=T)
head(edge_data)

dim <- dim(edge_data) 

long_data <- cbind(edge_data[,c("subject", "object")], rep(1, dim[1]))
colnames(long_data) <- c("subject", "object", "value")
head(long_data)

samples_subject <- grep("GOLD:ga", long_data$subject)
samples_object <- grep("GOLD:ga", long_data$object)

length(samples_subject)
length(samples_object)

#removing edges from sample to sample
long_data <- long_data[-samples_object,]
samples_subject <- grep("GOLD:ga", long_data$subject)
#only pick sample subjects
long_data <- long_data[samples_subject,]
dim(long_data)

wide_data <- reshape(data=long_data, idvar="subject", timevar="object", direction="wide")

write.table(wide_data, file="IMGVR_merged_kg_table.tsv", sep="\t")
