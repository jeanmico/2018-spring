setwd("/Volumes/Padlock/TOLSURF/")

subjects = read.table('filtered_wheeze.txt',sep='\t', header=TRUE)

png(filename="afr_wheeze.png")
boxplot(afr~wheeze, data=subjects, xlab="wheeze", ylab="afr", main="African ancestry")
dev.off()

png(filename="eur_wheeze.png")
boxplot(eur~wheeze, data=subjects, xlab="wheeze", ylab="eur", main="European ancestry")
dev.off()

png(filename="nam_wheeze.png")
boxplot(nam~wheeze, data=subjects, xlab="wheeze", ylab="nam", main="Native American ancestry")
dev.off()

wheeze_count = table(subjects$wheeze)
print(wheeze_count)

png(filename="afr_hist.png")
hist(subjects$afr, xlab='afr', main="African ancestry")
dev.off()

png(filename="eur_hist.png")
hist(subjects$eur, xlab='eur', main="European ancestry")
dev.off()

png(filename="nam_hist.png")
hist(subjects$nam, xlab='nam', main="Native American ancestry")
dev.off()

wheeze_yes = subset(subjects, wheeze==1)
wheeze_no = subset(subjects, wheeze==0)
wheeze_unknown = subset(subjects, wheeze==-1)

png(filename='afr_2hist.png')
hist(wheeze_no$afr, col=rgb(1,0,0,0.5), main="African ancestry", xlab = 'afr')
hist(wheeze_yes$afr, col=rgb(0,0,1,0.5), add=T)
dev.off()