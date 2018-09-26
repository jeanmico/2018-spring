# HOW TO CALL THIS CODE
# python data_process.py Race Ethnicity Remove_multiples Outfile_name
import os
import sys

def process():
    args = sys.argv[1:]
    race = args[0].lower()
    ethnicity = args[1].lower()
    remove_mult = False
    if args[2][0]=="T":
        remove_mult = True
    outprefix = args[3]

    filepath = os.path.join(os.path.sep, '/Volumes', 'Padlock', 'TOLSURF')
    outpath = os.path.join(filepath, outprefix)
    outfile = outprefix + '_subjects.txt'
    outrecord = outprefix + '_readme.txt'
    mainfile = 'ancestry_wheeze.txt'
    headerfile = 'headers.txt'
    multifile = 'tolsurf_twins_iid2.txt'
    filter_list = []  # stores numbers removed from population

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
    print('total subjects: ' + str(len(subjects)))
    total_subj = ['total subjects', str(len(subjects))]
    filter_list.append(total_subj)


    # filter out multiples
    if remove_mult:
        subjects, new_record = multiples(filepath, hdr, subjects, labid)
    filter_list.append(new_record)

    # filter by race
    if race.lower() != 'all':
        subjects, new_record = remove(hdr, subjects, 'APDRACE', race)
    filter_list.append(new_record)

    # filter by ethnicity
    if ethnicity.lower() != 'all':
        subjects, new_record = remove(hdr, subjects, 'APDETH', ethnicity)
    filter_list.append(new_record)

    # write output file
    output(outpath, outfile, subjects, headers)
    record_file(outpath, outrecord, filter_list)


def remove(hdr, data, column, value):
    #general function to filter out subjects
    # value is a collection 
    remove_ids = set()
    for key, val in data.items():
        if val[hdr[column]].lower()!=value:
            remove_ids.add(key)

    for identity in remove_ids:
        del data[identity]
    print(value + ': ' + str(len(data)))
    record = [value, str(len(data))]
    return data, record

    #TODO: print result
    #TODO: check length

def multiples(filepath, hdr, data, labid):
    # remove multiples by id
    multifile = 'tolsurf_twins_iid2.txt'
    multiples = set()
    with open(os.path.join(filepath, multifile), 'r') as f:
        for line in f:
            linevals = line.strip().split('\t')
            multiples.add(linevals[0])

    remove_ids = set()
    for key, val in data.items():
        if val[hdr['lab_id']] in multiples:
            remove_ids.add(val[hdr['lab_id']])

    for multiple_id in remove_ids:
        del data[labid[multiple_id]]
    # all the multiples were successfully removed
    print('remove multiples: ' + str(len(data)))
    record = ['remove multiples', str(len(data))]
    return data, record


def output(filepath, outfile, subjects, headers):
    # create output file that can be read into R
    with open(os.path.join(filepath, outfile), 'w+') as out:
        out.write('\t'.join(str(x) for x in headers))
        out.write('\n')
        out.write('\n'.join('\t'.join(str(x) for x in val) for val in subjects.values()))

def record_file(filepath, filename, data):
    with open(os.path.join(filepath, filename), 'w+') as out:
        out.write('\n'.join(': '.join(str(x) for x in item) for item in data))


if __name__ == '__main__':
    process()
