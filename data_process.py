import os
import sys

args = sys.argv[1:]

filepath = os.path.join(os.path.sep, '/Volumes', 'Padlock', 'TOLSURF')
mainfile = 'ikaria_pheno_data_ALL_withAncestry.txt'
headerfile = 'headers.txt'
multifile = 'tolsurf_twins_iid2.txt'

# create header dictionary
hdr = dict()
with open(os.path.join(filepath, headerfile), 'r') as f:
    for i, line in enumerate(f.readlines()):
        hdr[line.strip()] = i

subjects_all = dict()
with open(os.path.join(filepath, mainfile), 'r') as f:
    for line in f:
        linevals = line.strip().split('\t')
        subjects_all[linevals[0]] = linevals

# verify that there are no duplicate keys
if len(subjects_all) != len(set(subjects_all.keys())):
    raise ValueError('there are duplicate patient ids in the file')

# identify subjects of interest
subjects = dict()
for key, val in subjects_all.items():
    if val[hdr['APDRACE']] == 'Black or African American':
        subjects[key] = val

print(len(subjects))

# remove multiples by id
remove_ids = set()
with open(os.path.join(filepath, multifile), 'r') as f:
    for line in f:
        linevals = line.strip().split('\t')
        remove_ids.add(linevals[0])

for key, val in subjects.items():
    if val[hdr['lab_id']] in remove_ids:
        print('multiple')
