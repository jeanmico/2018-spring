import os
import sys
import csv
from bs4 import BeautifulSoup
from math import floor
from math import ceil

filepath = os.path.join(os.path.sep, "Volumes", "Padlock", "TOLSURF")
filename = "annual_aqi_by_county_2016.csv"
statefile = 'state_dict.txt'
sitefile = 'sites.csv'
mapfile = 'USA_Counties_with_names.svg'
outfile = "epa"
imgdir = os.path.join(filepath, 'epa')
missingfile = 'county_not_found.txt'

# state abbreviations needed to link epa data to svg map
state_abv = {}
with open(os.path.join(filepath, statefile)) as f:
    for line in f:
        lineval = line.strip().split(',')
        state = lineval[0]
        abv = lineval [1]

        state_abv[state]=abv

# read in the air quality data from the epa file
aqi = {}
labels = []
reader = csv.reader(open(os.path.join(filepath, filename)), delimiter = ",")
for row in reader:
    if row[0] == 'State':
        labels = [x.replace(' ', '_') for x in row[4:]]
    try:
        county = state_abv[row[0].upper()] + '_' +  row[1].strip().replace(' ', '_').replace("'", '').replace("Saint_", 'St._')
        quality = [int(x) for x in row[4:]]
        aqi[county] = quality
    except:
        pass

print(labels)

# identify the counties of interest; these will be outlined
sites = set()
reader = csv.reader(open(os.path.join(filepath, sitefile)), delimiter = ",")
for row in reader:
    if row[2] != '':
        sites.add(row[2] + '_' + row[3].replace(' ', '_'))

map_svg = open(os.path.join(filepath, mapfile), 'r').read()

soup = BeautifulSoup(map_svg, 'html.parser') 

paths = soup.findAll('path')

#color scheme pulled from colorbrewer
#TODO: make this finer graded
colors = ['#ffffcc','#ffeda0','#fed976','#feb24c','#fd8d3c','#fc4e2a','#e31a1c','#bd0026','#800026']
#replace entire style node with the following:
path_style = "font-size:12px;fill-opacity:1;fill-rule:nonzero;stroke:none;fill:"
path_style_b = "font-size:12px;fill-opacity:1;fill-rule:nonzero;stroke:blue;fill:"

missing_counties = set(aqi.keys())
# we want to know what entries are in the aqi list that were not colored on the map

for i, data_measure in enumerate(labels):
    # find maximum value to weight scores
    score_lst = list(aqi.values())
    score_max = max([score_lst[j][i] for j in range(len(score_lst))])
    score_min = min([score_lst[j][i] for j in range(len(score_lst))])

    # color step size
    step = ceil((score_max - score_min)/len(colors))

    map_svg = open(os.path.join(filepath, mapfile), 'r').read()
    soup = BeautifulSoup(map_svg, 'html.parser') 
    paths = soup.findAll('path')


    for p in paths:
        if p['id'] not in ['State_Lines', 'separator']:
            # try to match counties
            try:
                score = aqi[p['id']][i]
                if i == len(labels) - 1:
                    missing_counties.remove(p['id'])
            except:
                continue

            # create color fill
            if score == score_min:
                color_class = 0
            else:
                color_class = floor((score - score_min - 1)/step)

            color = colors[color_class]

            # modify color fill and outline counties of interest
            if p['id'] in sites:
                p['style'] = path_style_b + color
            else:
                p['style'] = path_style + color

    #create outfile
    with open(os.path.join(imgdir, outfile + '_' + data_measure + '.svg'), 'w+') as out:
        out.write(soup.prettify())



#record the counties we could not identify
with open(os.path.join(filepath, missingfile), 'w+') as missing:
    missing.write('\n'.join(x for x in missing_counties))

print('counties with aqi data: ' + str(len(aqi)))
print('counties with aqi not in svg map: ' + str(len(missing_counties)))

