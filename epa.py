import os
from matplotlib import pyplot as plt

filepath = os.path.join(os.path.sep, 'Users', 'student', 'Documents', '2018-spring')
filename = "annual_aqi_by_county_2016.csv"
medians = []
with open(os.path.join(filepath, filename)) as f:
    for line in f:
        lineval = line.strip().split(',')
        if lineval[0][1:-1] != "State":
            print(lineval[0])
            medians.append((lineval[0][1:-1], lineval[1][1:-1], int(lineval[12])))
print(medians)

fig, ax = plt.subplots()
