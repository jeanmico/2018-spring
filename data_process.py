import os
import sys

def process():
    args = sys.argv[1:]
    race = args[0]
    ethnicity = args[1]
    remove_mult = False
    if args[2][0]=="T":
        remove_mult = True

    filepath = os.path.join(os.path.sep, '/Volumes', 'Padlock', 'TOLSURF')
    mainfile = 'ancestry_wheeze.txt'
    headerfile = 'headers.txt'
    multifile = 'tolsurf_twins_iid2.txt'
    outfile = 'filtered_wheeze_whitehisp.txt'

    # create header dictionary
    headers = []
    hdr = dict()
    with open(os.path.join(filepath, headerfile), 'r') as f:
        for i, line in enumerate(f.readlines()):
            hdr[line.strip()] = i
            headers.append(line.strip())
    headers.append('wheeze')

    subjects = dict()
    ids_all = []
    labid = dict()
    with open(os.path.join(filepath, mainfile), 'r') as f:
        for line in f:
            linevals = line.strip().split('\t')
            tmpid = linevals[0]
            subjects[tmpid] = linevals
            ids_all.append(tmpid)
            labid[linevals[hdr['lab_id']]] = tmpid

    # verify that there are no duplicate keys
    if len(subjects) != len(ids_all):
        raise ValueError('there are duplicate patient ids in the file')
    print('Total subjects: ' + str(len(subjects)))

    # filter out multiples
    multiples(filepath, hdr, subjects, labid)

    # filter by race
    remove(hdr, subjects, 'APDRACE', race)

    # filter by ethnicity
    remove(hdr, subjects, 'APDETH', ethnicity)

    # write output file
    output(filepath, outfile, subjects, headers)


def remove(hdr, data, column, value):
    #general function to filter out subjects
    # value is a collection 
    remove_ids = set()
    for key, val in data.items():
        if val[hdr[column]]!=value:
            remove_ids.add(key)

    for identity in remove_ids:
        del data[identity]

    #TODO: print result
    #TODO: check length

def multiples(filepath, hdr, subjects, labid):
    # remove multiples by id
    multifile = 'tolsurf_twins_iid2.txt'
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
        del subjects[labid[multiple_id]]
    # all the multiples were successfully removed
    print('Remove multiples: ' + str(len(subjects)))


def output(filepath, outfile, subjects, headers):
    # create output file that can be read into R
    with open(os.path.join(filepath, outfile), 'w+') as out:
        out.write('\t'.join(str(x) for x in headers))
        out.write('\n')
        out.write('\n'.join('\t'.join(str(x) for x in val) for val in subjects.values()))

if __name__ == '__main__':
    process()
