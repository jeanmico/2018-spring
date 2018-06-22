setwd('/Volumes/Padlock/TOLSURF')
subjects = read.table('filtered_wheeze_numeric.txt', sep='\t', header=TRUE)

# remove subjects for which wheeze status is unknown
subjects = subset(subjects, wheeze != -1)
#TODO: check dimensions

subjects = subset(subjects, bpd36.die=='Yes')

#remove subjects for which an ancestry value is NA

cov = c('wheeze', 'afr', 'nam', 'eur', 'AE1GESAGE', 'AIDGEND', 'APDMGES', 'AIDWTG', 'APDRACE', 'APDETH')

num = c('afr', 'nam', 'eur', 'AE1GESAGE', 'AIDWTG')
num_translated = c('afr', 'nam', 'eur', 'AE1GESAGE', 'AIDGEND', 'APDMGES', 'AIDWTG', 'APDRACE', 'APDETH')

subjects = subjects[, cov]
subjects = subjects[complete.cases(subjects), ]

bpd = subjects[, num]

library(ggfortify)
png('pca_plt.png')
autoplot(prcomp(bpd), data=subjects, colour = 'wheeze')
dev.off()

bpd = subjects[, num_translated]

png('pca_complete.png')
autoplot(prcomp(bpd), data=subjects, colour = 'wheeze')
dev.off()

train_size = floor(0.75 * nrow(subjects))
train_ind = sample(seq_len(nrow(subjects)), size = train_size)
train = subjects[train_ind, ]
test = subjects[-train_ind, ]

mylogit = glm(wheeze ~ afr + nam + eur + AE1GESAGE + AIDGEND + APDMGES + AIDWTG + APDRACE + APDETH, data=train, family='binomial')

print(summary(mylogit))

library(pROC)
predict(mylogit, newdata=test, type='response')
library('ROCR')
prob = predict(mylogit, newdata=test, type='response')
pred = prediction(prob, test$wheeze)
perf = performance(pred, measure = 'tpr', x.measure = 'fpr')

auc = performance(pred, measure ='auc')
auc = auc@y.values[[1]]

png('bpd_wheeze_roc.png')
plot(perf, main=paste('AUROC = ', auc))
dev.off()
