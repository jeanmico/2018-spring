setwd("/Volumes/Padlock/TOLSURF/")

# THINGS TO UPDATE BEFORE RUNNING
subjects = read.table('filtered_wheeze_all.txt',sep='\t', header=TRUE)  # file to be read in, update
setwd("/Volumes/Padlock/TOLSURF/all")  # directory for saving plots, update
prefix = 'all_' # prefix for labelling plots, update

# subset the subjects by wheeze status
wheeze_yes = subset(subjects, wheeze==1)
wheeze_no = subset(subjects, wheeze==0)
wheeze_unknown = subset(subjects, wheeze==-1)

# BOXPLOTS
#2-sample t-test; see if we have significance
a = t.test(wheeze_yes$afr, wheeze_no$afr, var.equal=TRUE, paired=FALSE)
png(filename= paste(prefix, "afr_wheeze.png", sep=''))
boxplot(afr~wheeze, data=subjects, xlab="wheeze", ylab="afr", main=paste("African ancestry", '(pval = ', round(a$p.value,2), ')'))
dev.off()

#2-sample t-test; see if we have significance
a = t.test(wheeze_yes$eur, wheeze_no$eur, var.equal=TRUE, paired=FALSE)
png(filename=paste(prefix, "eur_wheeze.png", sep=''))
boxplot(eur~wheeze, data=subjects, xlab="wheeze", ylab="eur", main=paste("European ancestry", '(pval = ', round(a$p.value,2), ')'))
dev.off()

#2-sample t-test; see if we have significance
a = t.test(wheeze_yes$nam, wheeze_no$nam, var.equal=TRUE, paired=FALSE)
png(filename=paste(prefix, "nam_wheeze.png", sep=''))
boxplot(nam~wheeze, data=subjects, xlab="wheeze", ylab="nam", main=paste("Native American ancestry", '(pval = ', round(a$p.value,2), ')'))
dev.off()

# WHEEZE STATUS
wheeze_count = table(subjects$wheeze)
print(wheeze_count)

# ANCESTRY HISTOGRAMS

png(filename=paste(prefix, 'afr_hist.png', sep=''))
hist(subjects$afr, xlab='afr', main="African ancestry")
dev.off()


png(filename=paste(prefix, 'eur_hist.png', sep=''))
hist(subjects$eur, xlab='eur', main="European ancestry")
dev.off()


png(filename=paste(prefix, 'nam_hist.png', sep=''))
hist(subjects$nam, xlab='nam', main="Native American ancestry")
dev.off()




# multi-layer histogram, not that helpful
#png(filename='afr_2hist.png')
#hist(wheeze_no$afr, col=rgb(1,0,0,0.5), main="African ancestry", xlab = 'afr')
#hist(wheeze_yes$afr, col=rgb(0,0,1,0.5), add=T)
#dev.off()

# wheeze status known, used for logistic regression
wheeze_known = subset(subjects, wheeze!=-1)

train_size = floor(0.75 * nrow(wheeze_known))

train_ind = sample(seq_len(nrow(wheeze_known)), size = train_size)
train = wheeze_known[train_ind, ]
test = wheeze_known[-train_ind, ]


# logistic regression model
mylogit = glm(wheeze ~ afr + nam + AE1GESAGE + AIDGEND + APDMGES + AIDWTG + APDRACE + APDETH, data=train, family="binomial")
summary(mylogit)

# area under the curve
library(pROC)
predict(mylogit, newdata=test, type='response')

library('ROCR')
prob = predict(mylogit, newdata=test, type="response")
pred = prediction(prob, test$bpd36.die)
perf = performance(pred, measure = 'tpr', x.measure = 'fpr')

auc = performance(pred, measure = 'auc')
auc = auc@y.values[[1]]
auc

png(filename=paste(prefix, "roc_afrnam.png", sep=''))
plot(perf, main=paste('AUROC =', auc))
dev.off()



