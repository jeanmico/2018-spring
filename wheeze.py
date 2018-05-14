import os
import sys

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def id_match(wheeze, ancestry):
    for pheno in wheeze:
        patient = pheno[0]
        if patient in ancestry:
            ancestry[patient].append(pheno[1])
        else:
            print(patient)

filepath = os.path.join(os.path.sep, 'Volumes', 'Padlock', 'TOLSURF')
wheezefile = 'wheeze.csv'
ancestryfile = 'ikaria_pheno_data_ALL_withAncestry.txt'
outfile = 'ancestry_wheeze.txt'

ancestry = dict()
with open(os.path.join(filepath, ancestryfile), 'r') as f:
    for line in f:
        lineval = line.strip().split('\t')
        if lineval[0] != 'RANDN':
            ancestry[lineval[1]] = lineval

wheeze_id = set()
wheeze = []
with open(os.path.join(filepath, wheezefile), 'r') as f:
    for line in f:
        lineval = line.strip().split(',')
        patient = lineval[0].strip()
        if is_number(patient):
            wheeze_id.add(patient)
            wheeze.append(lineval)

if len(wheeze_id) != len(wheeze):
    raise ValueError('duplicate id found in wheeze file')

id_match(wheeze, ancestry)

# write output
with open(os.path.join(filepath, outfile), 'w+') as out:
        out.write('\n'.join('\t'.join(str(x) for x in val) for val in ancestry.values()))
