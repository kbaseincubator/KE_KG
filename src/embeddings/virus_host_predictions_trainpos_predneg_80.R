rm(list=ls())
set.seed(12345)

library("randomForest")
library("randomForestExplainer")
library("caTools")
library ("ROCR")
#library("data.table")#fmatch

#setwd("~/graphs/KE_KG")
#node_data <- read.csv("/global/cfs/cdirs/kbase/ke_prototype/KE_KG/data/merged/merged_imgvr_mg_nodes.tsv", sep="\t",header=T)
setwd("~/Documents/KBase/KE/IMGVR/")
#node_data <- read.csv("./IMGVR_merged_kg_nodes.tsv", sep="\t",header=T)
node_data <- read.csv("./link_predict_mg_imgvr_OPT_v4/IMGVR_merged_kg_nodes__positive80_v4.tsv", sep="\t",header=T)

dim(node_data)
head(node_data) 

node_labels <- as.character(node_data$id)


#virus_host_positive <- read.csv("./link_predict/virus_host__subtract.tsv", row.names=1)
virus_host_positive <- read.csv("./link_predict_mg_imgvr_OPT_v4_80/virus_host__subtract.tsv", row.names=1, header=TRUE, sep=",")
virus_host_positive_labels <- read.csv("./link_predict_mg_imgvr_OPT_v4_80/virus_host__subtract_labels.tsv")
dim(virus_host_positive)
dim(virus_host_positive_labels)
head(virus_host_positive_labels)
#head(virus_host_positive)
dimpos <- dim(virus_host_positive)
dimpos



virus_host_negative <- read.csv("./link_predict_mg_imgvr_OPT_v4_80/virus_host_NEGATIVE__subtract.tsv", row.names=1, header=TRUE, sep=",")
virus_host_negative_labels <- read.csv("./link_predict_mg_imgvr_OPT_v4_80/virus_host_NEGATIVE__subtract_labels.tsv")
head(virus_host_negative)
dim(virus_host_negative)
sum(is.na(virus_host_negative))
dim(virus_host_negative_labels)
#head(virus_host_negative)
dimneg <- dim(virus_host_negative)
#head(virus_host_negative)
#row.names(virus_host_negative) <- virus_host_negative_labels[,1]


virus_host_new <- read.csv("./link_predict_mg_imgvr_OPT_v4_80/virus_host_NEW__subtract.tsv", row.names=1, header=TRUE, sep=",")
virus_host_new_labels <- read.csv("./link_predict_mg_imgvr_OPT_v4_80/virus_host_NEW_subtract_labels.tsv")
dim(virus_host_new)
sum(is.na(virus_host_new))
dim(virus_host_new_labels)
#head(virus_host_new)
dimnew <- dim(virus_host_new)
#head(virus_host_new)
row.names(virus_host_new) <- virus_host_new_labels[,1]


#print("trimming positive because FEWER NEGATIVE!!!")
#virus_host_positive <- virus_host_positive[1:dimneg[1],]
#class(virus_host_positive_labels)
#virus_host_positive_labels <- virus_host_positive_labels[1:dimneg[1],]
#dim(virus_host_positive)
#dim(virus_host_positive_labels)
#length(virus_host_positive_labels)
#row.names(virus_host_positive) <- virus_host_positive_labels
#dimpos <- dim(virus_host_positive)
#dimpos

sum(is.na(virus_host_positive))
sum(is.na(virus_host_negative))





virus_host_test <- read.csv("./link_predict_mg_imgvr_OPT_v4/IMGVR_sample_extra_test.txt", row.names=1, header=TRUE, sep="\t")
virus_host_test_labels <- read.csv("./link_predict_mg_imgvr_OPT_v4/IMGVR_sample_extra_test_edges_labels.txt")
dim(virus_host_test)
head(virus_host_test)
sum(is.na(virus_host_test_labels))
dim(virus_host_test_labels)
#head(virus_host_negative)
dimtest <- dim(virus_host_test)
#head(virus_host_negative)
row.names(virus_host_test) <- virus_host_test_labels[,1]

test_split <- strsplit(row.names(virus_host_test) , "\t")
test_labels  <- unlist(test_split)[2*(1:length(test_split))  ]
head(test_labels)

match_test_pos <- match(test_labels, row.names(virus_host_positive))
match_test_pos_rev <- match(test_labels, row.names(virus_host_positive))
head(match_test_train)
sum(is.na(match_test_train))

match_test_neg <- match(test_labels, row.names(virus_host_negative))
head(match_test_neg)
sum(is.na(match_test_neg))


test_pos_final <- virus_host_positive[match_test_pos[which(!is.na(match_test_pos))], ]
train_pos_final <- virus_host_positive[-match_test_pos[which(!is.na(match_test_pos))],]
test_neg <- 0.2*dimneg[1]
test_neg_index <- runif(round(test_neg), 1, dimneg[1])
length(test_neg_index)
train_neg_final <- virus_host_negative[-test_neg_index,]
test_neg_final <- virus_host_negative[test_neg_index,]
dim(test_pos_final)
dim(test_neg_final)

total_train_data <- rbind(train_pos_final, train_neg_final)
###limit to top features
#total_train_data <- total_train_data[,c(45, 82, 44,45, 90, 0, 3,7, 60, 70, 88, 39, 59, 56,94,97, 17)]
dim(total_train_data)
#head(total_train_data)
sum(is.na(total_train_data))

pos_neg_label <- c(rep(1, dim(train_pos_final)[1]), rep(0, dim(train_neg_final)[1]))
names(pos_neg_label) <- "pos_neg"
total_train_data <- cbind(total_train_data, pos_neg_label)
dim(total_train_data)

total_test_data <- rbind(test_pos_final, test_neg_final)
pos_neg_label_test <- rep(0, dim(total_test_data)[1])
pos_neg_label_test[which(match_test_pos > 0)] <- 1
names(pos_neg_label_test) <- "pos_neg"
total_test_data <- cbind(total_test_data, pos_neg_label_test)
dim(total_test_data)


#virus_host_positive <- read.csv("./link_predict/virus_host__subtract.tsv", row.names=1)
virus_host_positive_ALL <- read.csv("./link_predict_mg_imgvr_OPT_v4/virus_host__subtract.tsv", row.names=1, header=TRUE, sep=",")
virus_host_positive_ALL_labels <- read.csv("./link_predict_mg_imgvr_OPT_v4/virus_host__subtract_labels.tsv")
dim(virus_host_positive_ALL)
dim(virus_host_positive_ALL_labels)
#head(virus_host_positive)
dimposALL <- dim(virus_host_positive_ALL)
dimposALL




###convert response variable to factor for classification
###otherwise random forest regression model
rf_classifier <- randomForest(as.factor(pos_neg_label) ~ ., data=total_train_data, ntree=50, replace=TRUE, proximity=FALSE, importance=TRUE,do.trace=TRUE)
#rf_classifier <- randomForest(y=as.factor(train[,'pos_neg_label']), x=train[, 1:(dimtrain[2]-1)], ntree=200, replace=FALSE, proximity=TRUE, importance=TRUE,do.trace=TRUE)

rf_classifier
varImpPlot(rf_classifier)

predict_train <- predict(rf_classifier,total_train_data)
length(predict_train)
table(observed=total_train_data[,65],predicted=predict_train)#

dim(total_test_data)
head(total_test_data)
prediction_for_table <- predict(rf_classifier,total_test_data)
length(prediction_for_table)
dim(total_test_data)
class(total_test_data)
colnames(total_test_data)
table(observed=total_test_data[,65],predicted=prediction_for_table)#pos_neg_label


####

head(total_test_data)
y <- total_test_data[,'pos_neg_label_test']#... # logical array of positive / negative cases
predictions <- prediction_for_table # array of predictions
class(predictions)
pred <- prediction(as.numeric(as.character(predictions)), y);

# Recall-Precision curve             
RP.perf <- performance(pred, "prec", "rec");

pdf(file = "virus_host_RF_recall_precision.pdf", width = 11, height = 8)
plot (RP.perf);
dev.off()

# ROC curve
ROC.perf <- performance(pred, "tpr", "fpr");
pdf(file = "virus_host_RF_ROC.pdf", width = 11, height = 8)
plot (ROC.perf);
dev.off()


# ROC area under the curve
auc.tmp <- performance(pred,"auc");
auc <- as.numeric(auc.tmp@y.values)
dev.off()


min_depth_frame <- min_depth_distribution(rf_classifier)

save.image(file='randomForest_v0.01_v4')



write.table(total_train_data, file="virus_host_train_20200308.txt", sep="\t")
write.table(total_test_data, file="virus_host_test_20200308.txt", sep="\t")



####


###predict on negative train
prediction_for_table2 <- predict(rf_classifier,virus_host_negative)
length(prediction_for_table2)

prediction_for_table2[which(prediction_for_table2 == 1)]

write.table(prediction_for_table2, file="virus_host_predict_NEW_links_on_negtrain.txt", sep="\t")


###predict on positive train
prediction_for_table3 <- predict(rf_classifier,virus_host_positive)
length(prediction_for_table3)

prediction_for_table2[which(prediction_for_table3 == 1)]

write.table(prediction_for_table3, file="virus_host_predict_NEW_links_on_postrain.txt", sep="\t")


#virus_host_new
prediction_for_table4 <- predict(rf_classifier,virus_host_new)
length(prediction_for_table4)

prediction_for_table4[which(prediction_for_table4 == 1)]

write.table(prediction_for_table4, file="virus_host_predict_NEW_links_on_rand10new.txt", sep="\t")


