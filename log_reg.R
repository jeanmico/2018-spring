setwd('/Volumes/Padlock/TOLSURF')
subjects = read.table('filtered_data.txt', sep='\t', header=TRUE)
set.seed(100)

train_size = floor(0.75 * nrow(subjects))

train_ind = sample(seq_len(nrow(subjects)), size = train_size)
train = subjects[train_ind, ]
test = subjects[-train_ind, ]

mylogit = glm(bpd36.die ~ afr + nam + AE1GESAGE + AIDGEND + APDMGES + AIDWTG, data=train, family="binomial")
summary(mylogit)

library(pROC)
predict(mylogit, newdata=test, type='response')


library('ROCR')
prob = predict(mylogit, newdata=test, type="response")
pred = prediction(prob, test$bpd36.die)
perf = performance(pred, measure = 'tpr', x.measure = 'fpr')
plot(perf)

auc = performance(pred, measure = 'auc')
auc = auc@y.values[[1]]
auc
