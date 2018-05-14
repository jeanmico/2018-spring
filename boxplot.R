setwd("/Volumes/Padlock/TOLSURF/")

subjects = read.table('filtered_wheeze.txt',sep='\t', header=TRUE)

boxplot(afr~wheeze, data=subjects)
