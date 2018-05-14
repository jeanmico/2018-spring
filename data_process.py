import os
import sys

args = sys.argv[1:]

filepath = os.path.join(os.path.sep, '/Volumes', 'Padlock', 'TOLSURF')
mainfile = 'ancestry_wheeze.txt'
headerfile = 'headers.txt'
multifile = 'tolsurf_twins_iid2.txt'
outfile = 'filtered_wheeze.txt'

# create header dictionary
headers = []
hdr = dict()
with open(os.path.join(filepath, headerfile), 'r') as f:
    for i, line in enumerate(f.readlines()):
        hdr[line.strip()] = i
        headers.append(line.strip())
headers.append('wheeze')

subjects_all = dict()
with open(os.path.join(filepath, mainfile), 'r') as f:
    for line in f:
        linevals = line.strip().split('\t')
        subjects_all[linevals[0]] = linevals

# verify that there are no duplicate keys
if len(subjects_all) != len(set(subjects_all.keys())):
    raise ValueError('there are duplicate patient ids in the file')

# identify subjects of interest
#TODO: create output file of removed ids
subjects = dict()
labid_id = dict()
na_count = 0
for key, val in subjects_all.items():
    if val[hdr['APDRACE']] == 'Black or African American':
        subjects[key] = val
        labid_id[val[hdr['lab_id']]] = key
        if val[hdr['lab_id']] == 'NA':
            na_count += 1

print(len(subjects))
print(len(labid_id))  # 38 subjects for which the ID is NA
print(na_count)

# remove multiples by id
multiples = set()
with open(os.path.join(filepath, multifile), 'r') as f:
    for line in f:
        linevals = line.strip().split('\t')
        multiples.add(linevals[0])

remove_ids = set()
for key, val in subjects.items():
    if val[hdr['lab_id']] in multiples:
        remove_ids.add(val[hdr['lab_id']])

for multiple_id in remove_ids:
    del subjects[labid_id[multiple_id]]
# all the multiples were successfully removed

# remove Hispanic/Latino
hisp_ids = set()
for key, val in subjects.items():
    if val[hdr['APDETH']] == 'Hispanic or Latino':
        hisp_ids.add(key)
print(len(hisp_ids))

for hisp in hisp_ids:
    del subjects[hisp]

print(len(subjects))    
# create output file that can be read into R
with open(os.path.join(filepath, outfile), 'w+') as out:
    out.write('\t'.join(str(x) for x in headers))
    out.write('\n')
    out.write('\n'.join('\t'.join(str(x) for x in val) for val in subjects.values()))
