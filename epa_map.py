import os
import sys
import csv
#from beautifulsoup4 import beautifulsoup
#import beautifulsoup4
from bs4 import BeautifulSoup

filepath = os.path.join(os.path.sep, "Users", "student", "Downloads")
filename = "annual_aqi_by_county_2016.csv"
statefile = 'state_dict.txt'
mapfile = 'USA_Counties_with_FIPS_and_names.svg'

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
        county = row[1].upper() + ', ' + state_abv[row[0].upper()]
        quality = int(row[12])
        aqi[county] = quality
    except:
        pass
print(aqi)

map_svg = open(os.path.join(filepath, mapfile), 'r').read()

soup = BeautifulSoup(map_svg, selfClosingTags=['defs', 'sodipodi:namedview'])

paths = soup.findAll('path')

print(paths)
