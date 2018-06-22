import os
from collections import defaultdict

dictfile = "string_to_num.tsv"
datafile = "filtered_wheeze_all.txt"
filepath = os.path.join(os.path.sep, "Volumes", "Padlock", "TOLSURF")
outfile = "filtered_wheeze_numeric.txt"

translate = defaultdict(dict)
with open(os.path.join(filepath, dictfile), 'r') as f:
    for line in f:
        vals = line.strip().split('\t')
        translate[vals[0]][vals[1] ]= vals[2]

headers = dict()
head_list = []
data = []
with open(os.path.join(filepath, datafile), 'r') as f:
    for line in f:
        vals = line.strip().split('\t')
        if vals[0] == "RANDN":
            head_list = vals
            for i, item in enumerate(vals):
                headers[i] = item
        else:
            data.append(vals)

subjects_numeric = []
for subject in data:
    new_subj = []
    for i, item in enumerate(subject):
        if headers[i] in translate:
            tmp = translate[headers[i]][item]
            new_subj.append(tmp)
        else:
            new_subj.append(item)
    subjects_numeric.append(new_subj)
            
with open(os.path.join(filepath, outfile), 'w+') as o:
    o.write('\t'.join(str(x) for x in head_list))
    o.write('\n')
    o.write('\n'.join('\t'.join(str(x) for x in row) for row in subjects_numeric))
