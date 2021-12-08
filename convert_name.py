# Load the polyinfo_viscosity.csv rows with 'name|viscosity'
# and run this script, the output will be in processed_viscosity.csv

from urllib.request import urlopen
from urllib.parse import quote
import csv

def CIRconvert(ids):
    try:
        url = 'http://cactus.nci.nih.gov/chemical/structure/' + quote(ids) + '/smiles'
        ans = urlopen(url).read().decode('utf8')
        return ans
    except:
        return 'Did not work'

polymers = []

with open('polyinfo_viscosity.csv', newline='') as csvfile:
    r = csv.reader(csvfile, delimiter='|')
    next(r) # skip the first row
    for row in r:
        polymers.append([row[0],row[1]])

with open('processed_viscosity.csv', 'w', newline='') as csvfile:
    w = csv.writer(csvfile, delimiter=',')
    w.writerow(["SMILES", "melt viscosity"])
    for ids in polymers :
        # print(ids)
        result = CIRconvert(ids[0])
        if result != 'Did not work':
            w.writerow([result, ids[1]])
            print("write: ", result, ids[1])