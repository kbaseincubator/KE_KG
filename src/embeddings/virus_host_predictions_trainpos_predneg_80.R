rm(list=ls())
set.seed(12345)

library("randomForest")
library("caTools")
library ("ROCR")
#library("data.table")#fmatch

#setwd("~/graphs/KE_KG")
#node_data <- read.csv("/global/cfs/cdirs/kbase/ke_prototype/KE_KG/data/merged/merged_imgvr_mg_nodes.tsv", sep="\t",header=T)
setwd("~/Documents/KBase/KE/IMGVR/")
#node_data <- read.csv("./IMGVR_merged_kg_nodes.tsv", sep="\t",header=T)
node_data <- read.csv("./IMGVR_merged_kg_nodes__positive80.tsv", sep="\t",header=T)

dim(node_data)
head(node_data) 

node_labels <- as.character(node_data$id)


virus_host_positive <- read.csv("./link_predict_IMGVR_sample_extra_v3_80/virus_host__subtract.tsv", row.names=1, header=TRUE, sep=",")
virus_host_positive_labels <- read.csv("./link_predict_IMGVR_sample_extra_v3_80/virus_host__subtract_labels.tsv")
dim(virus_host_positive)
length(virus_host_positive_labels)
head(virus_host_positive)
dimpos <- dim(virus_host_positive)
dimpos


virus_host_negative <- read.csv("./link_predict_IMGVR_sample_extra_v3_80/virus_host_NEGATIVE__subtract.tsv", row.names=1, header=TRUE, sep=",")
virus_host_negative_labels <- read.csv("./link_predict_IMGVR_sample_extra_v3_80/virus_host_NEGATIVE__subtract_labels.tsv")
dim(virus_host_negative)
sum(is.na(virus_host_negative))
dim(virus_host_negative_labels)
head(virus_host_negative)
dimneg <- dim(virus_host_negative)
head(virus_host_negative)
dimneg
row.names(virus_host_negative) <- virus_host_negative_labels[,1]

virus_host_negative_naindex <- which(apply(virus_host_negative, 1, function(x) {sum(is.na(x))}) > 0)
virus_host_negative <- virus_host_negative[-virus_host_negative_naindex,]

virus_host_new <- read.csv("./link_predict_IMGVR_sample_extra_v3_80/virus_host_NEW__subtract.tsv", row.names=1, header=TRUE, sep=",")
virus_host_new_labels <- read.csv("./link_predict_IMGVR_samlink_predict_IMGVR_sample_extra_v3_80ple_extra_80/virus_host_NEW_subtract_labels.tsv")
dim(virus_host_new)
sum(is.na(virus_host_new))
dim(virus_host_new_labels)
head(virus_host_new)
dimnegnew <- dim(virus_host_new)
head(virus_host_new)
dimnegnew
row.names(virus_host_new) <- virus_host_new_labels[,1]


###
###
###

virus_host_positive_all <- read.csv("./link_predict_IMGVR_sample_extra/virus_host__subtract.tsv", row.names=1, header=TRUE, sep=",")
virus_host_positive_labels_all <- read.csv("./link_predict_IMGVR_sample_extra/virus_host__subtract_labels.tsv")
dim(virus_host_positive_all)
length(virus_host_positive_labels_all)
head(virus_host_positive_all)
dimpos_all <- dim(virus_host_positive_all)
dimpos_all


virus_host_negative_all <- read.csv("./link_predict_IMGVR_sample_extra/virus_host_NEGATIVE__subtract.tsv", row.names=1, header=TRUE, sep=",")
virus_host_negative_labels_all <- read.csv("./link_predict_IMGVR_sample_extra/virus_host_NEGATIVE__subtract_labels.tsv")
dim(virus_host_negative_all)
sum(is.na(virus_host_negative_all))
dim(virus_host_negative_labels_all)
head(virus_host_negative_all)
dimneg_all <- dim(virus_host_negative_all)
head(virus_host_negative_all)
dimneg_all
row.names(virus_host_negative_all) <- virus_host_negative_labels_all[,1]

virus_host_negative_naindex_all <- which(apply(virus_host_negative_all, 1, function(x) {sum(is.na(x))}) > 0)
virus_host_negative_all <- virus_host_negative_all[-virus_host_negative_naindex_all,]

virus_host_positive_all_diff_index <- which(is.na(match(virus_host_positive_labels_all, virus_host_positive_labels)))
virus_host_negative_all_diff_index <- which(is.na(match(virus_host_negative_labels_all, virus_host_negative_labels)))                                     
length(virus_host_positive_all_diff_index)
length(virus_host_negative_all_diff_index)

###
###
###


#print("trimming positive because FEWER NEGATIVE!!!")
#virus_host_positive <- virus_host_positive[1:dimneg[1],]
class(virus_host_positive_labels)
virus_host_positive_labels <- virus_host_positive_labels[1:dimneg[1],]
dim(virus_host_positive)
dim(virus_host_positive_labels)
length(virus_host_positive_labels)
#row.names(virus_host_positive) <- virus_host_positive_labels
dimpos <- dim(virus_host_positive)
dimpos
dimneg <- dim(virus_host_negative)
dimneg

sum(is.na(virus_host_positive))
sum(is.na(virus_host_negative))

total_train_data <- rbind(virus_host_positive, virus_host_negative)
dim(total_train_data)
head(total_train_data)
sum(is.na(total_train_data))
total_train_data_labels <- row.names(total_train_data)
head(total_train_data_labels)
class(class(train_data_labels))


total_train_data_all <- rbind(virus_host_positive_all, virus_host_negative_all)
total_train_data_all_labels <- row.names(total_train_data_all)


###
### NEW
###


test_data <- read.csv("IMGVR_sample_extra_test.txt", row.names=1, header=TRUE, sep="\t")
dim(test_data)
test_data_labels_split <- strsplit(row.names(test_data), "\t")
test_data_labels <- unlist(test_data_labels_split)[2*(1:length(test_data_labels_split))]#unlist(row.names(test_data))
length(test_data_labels)
head(test_data_labels)

train_data <- read.csv("IMGVR_sample_extra_train.txt", row.names=1, header=TRUE, sep="\t")
dim(train_data)
train_data_labels_split <- strsplit(row.names(train_data), "\t")
train_data_labels <- unlist(train_data_labels_split)[2*(1:length(train_data_labels_split))]#unlist(row.names(test_data))
length(train_data_labels)
head(train_data_labels)
class(train_data_labels)

test_match <- match(test_data_labels, total_train_data_labels)
train_match <- match(train_data_labels, total_train_data_labels)

test_data_labels[is.na(test_match)]

sum(is.na(test_match))
sum(!is.na(test_match))
sum(is.na(train_match))
sum(!is.na(train_match))



test_match_all <- match(test_data_labels, total_train_data_all_labels)
train_match_all  <- match(train_data_labels, total_train_data_all_labels)

test_data_labels[is.na(test_match_all)]

sum(is.na(test_match_all))
sum(!is.na(test_match_all))
sum(is.na(train_match_all))
sum(!is.na(train_match_all))


###
###
###


row.names(virus_host_negative)[which(apply(virus_host_negative, 1, function(x) { sum(is.na(x))}) > 0)]

pos_neg_label <- c(rep(1, dimpos[1]), rep(0, dimneg[1]))
names(pos_neg_label) <- "pos_neg"
total_train_data <- cbind(total_train_data, pos_neg_label)
dimtotal <- dim(total_train_data)
dimtotal
sum(is.na(total_train_data))

sample <- read.csv("IMGVR_sample_extra_sample.txt", row.names=1, header=TRUE, sep="\t")
sum(sample == FALSE)#8340
sum(sample==TRUE)#33362
dim(sample)
dim(total_train_data)
33362 + 8340

total_train_data_80 <- total_train_data[sample==TRUE, ]
total_train_data_20 <- total_train_data[sample==FALSE, ]
dim(total_train_data_80)
dim(total_train_data_20)

which(sum(is.na(total_train_data_80)) > 0)

narows <- which((grepl("NA", row.names(total_train_data_80))))
narows
row.names(total_train_data_80)[narows]
total_train_data_80[narows,]
total_train_data_80 <- total_train_data_80[-narows,]

row.names(total_train_data_80)
narows <- which(apply(total_train_data_80, 1, function(x) { sum(is.na(x))}) > 0)
print(narows)
row.names(total_train_data_80)[narows]



head(total_train_data_80)
sum(is.na(total_train_data_80))
#total_train_data
###convert response variable to factor for classification
###otherwise random forest regression model
#[,-dimtotal[2]]
rf_classifier <- randomForest(as.factor(pos_neg_label) ~ ., data=total_train_data_80, ntree=200, importance=TRUE,do.trace=TRUE)#mtry=sqrt(dimtrain[1]),
#rf_classifier <- randomForest(train[,'pos_neg_label'], data=train[, 1:(dimtrain[1]-1)], ntree=10, mtry=sqrt(dimtrain[1]), importance=TRUE,do.trace=TRUE)

rf_classifier
varImpPlot(rf_classifier)

#predict_train <- predict(rf_classifier,train)

prediction_for_table <- predict(rf_classifier,total_train_data_20)
length(prediction_for_table)
dim(test_data)
class(test_data)
colnames(test_data)
table(observed=test_data[,101],predicted=prediction_for_table)#pos_neg_label


####


y <- test_data[,'pos_neg_label']#... # logical array of positive / negative cases
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



save.image(file='randomForest_v0.01__IMGVR_sample_extra_80_v3')

