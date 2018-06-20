import os
import sys
import csv
from bs4 import BeautifulSoup
from math import floor

filepath = os.path.join(os.path.sep, "Volumes", "Padlock", "TOLSURF")
filename = "annual_aqi_by_county_2016.csv"
statefile = 'state_dict.txt'
mapfile = 'USA_Counties_with_names.svg'
outfile = "epa.svg"
missingfile = 'county_not_found.txt'

state_abv = {}
with open(os.path.join(filepath, statefile)) as f:
    for line in f:
        lineval = line.strip().split(',')
        state = lineval[0]
        abv = lineval [1]

        state_abv[state]=abv


aqi = {}
reader = csv.reader(open(os.path.join(filepath, filename)), delimiter = ",")
for row in reader:
    try:
        county = state_abv[row[0].upper()] + '_' +  row[1].strip().replace(' ', '_').replace("'", '').replace("Saint_", 'St._')
        quality = int(row[12])
        aqi[county] = quality
    except:
        pass

map_svg = open(os.path.join(filepath, mapfile), 'r').read()

soup = BeautifulSoup(map_svg, 'html.parser') 

paths = soup.findAll('path')

#color scheme pulled from colorbrewer
#TODO: make this finer graded
colors = ['#fef0d9','#fdd49e','#fdbb84','#fc8d59','#e34a33','#b30000']
#replace entire style node with the following:
path_style = "font-size:12px;fill-opacity:1;fill-rule:nonzero;stroke:none;fill:"

missing_counties = set(aqi.keys())
# we want to know what entries are in the aqi list that were not colored on the map
# in the api list but not in the paths...
for p in paths:
    if p['id'] not in ['State_Lines', 'separator']:
        try:
            score = aqi[p['id']]
            missing_counties.remove(p['id'])
        except:
            continue

        if score == 0:
            color_class = 0
        elif score > 100:
            color_class = -1
        else:
            color_class = floor((score - 1)/20)

        color = colors[color_class]
        p['style'] = path_style + color
#create outfile
with open(os.path.join(filepath, outfile), 'w+') as out:
    out.write(soup.prettify())

#record the counties we could not identify
with open(os.path.join(filepath, missingfile), 'w+') as missing:
    missing.write('\n'.join(x for x in missing_counties))

print('counties with aqi data: ' + str(len(aqi)))
print('counties with aqi not in svg map: ' + str(len(missing_counties)))

