import os

id_len = 0
with open(os.path.join(os.path.sep, 'Volumes', 'Padlock', 'TOLSURF', 'filtered_data.txt')) as f:
    for line in f:
        lineval = line.strip().split('\t')
        if len(lineval[0]) != id_len:
            print(id_len)
            id_len = len(lineval[0])
            print(id_len)
