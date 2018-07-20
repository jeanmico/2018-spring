args = commandArgs(trailingOnly=TRUE)

# INPUT ARGUMENTS

if (length(args) !=3) {
	stop("three arguments required")
}

infile = args[1] # name of file containing data to be analyzed
outpref = args[2] # defines prefix of the files to be written
airdata = FALSE # captures whether or not the EPA air quality data should be considered
if (substr(airdata,1,1) == 'T') {
	airdata = TRUE
}

# READ IN THE DATA

setwd("/Volumes/Padlock/TOLSURF/")
subjects = read.table(infile ,sep='\t', header=TRUE)  # file to be read in, update
setwd(paste("/Volumes/Padlock/TOLSURF/", outpref, sep=''))  # directory for saving plots, update
prefix = paste(outpref, '_', sep='') # prefix for labelling plots, update

anc = c('afr', 'eur', 'nam')
ancestry = c("African", "European", "Native American")

# subset the subjects by wheeze status
wheeze_yes = subset(subjects, wheeze==1)
wheeze_no = subset(subjects, wheeze==0)
wheeze_unknown = subset(subjects, wheeze==-1)

# BOXPLOTS
#2-sample t-test; see if we have significance
png(filename=paste(prefix, "_wheeze.png", sep=''), width=800,height=350)
par(mfrow=c(1,3))
for (i in 1:length(ancestry)) {
	a = t.test(wheeze_yes[anc[i]], wheeze_no[anc[i]], var.equal=TRUE, paired=FALSE)
	boxplot(subjects[,anc[i]]~subjects$wheeze, data=subjects, xlab="wheeze", ylab=anc[i], main=ancestry[i], sub=paste('pval =', round(a$p.value,2)))
	#dev.off()
}
dev.off()

# WHEEZE STATUS
wheeze_count = table(subjects$wheeze)
print(wheeze_count)

# ANCESTRY HISTOGRAMS

png(filename=paste(prefix, '_ancestry.png', sep=''), width=800, height=350)
par(mfrow=c(1,3))
for (i in 1:length(ancestry)) {
	hist(subjects[,anc[i]], xlab=anc[i], main=ancestry[i])
}
dev.off()

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



