__author__ = 'scottsfarley'
import API
import classes

import matplotlib.pyplot as plt
import shelve

dataset = API.getDatasetDownload(14410)
download = dataset.items[0]
samples = download.samples
taxa = []

for sample in samples:
    data = sample.sampleData
    for point in data:
        tName = point.taxonName
        if tName not in taxa:
            taxa.append(tName)

taxa = set(taxa)

data = {}
years = []
sums = []
ageUnits = ""


for i in samples:
    sample = i
    ages = sample.sampleAges
    years.append(ages[0].age)
    ageUnits = ages[0].ageType
    sampleDataList = sample.sampleData
    value1 = None
    value2 = None
    sum = 0
    levelTaxa = []
    for j in sampleDataList:
        tName = j.taxonName
        tValue = j.Value
        try:
            data[tName].append(tValue)
        except KeyError:
            data[tName] = []
            data[tName].append(tValue)
        levelTaxa.append(tName)
        sum += j.Value
    for t in taxa:
        if t in levelTaxa:
            pass
        else:
            try:
                data[t].append(0)
            except KeyError:
                data[t] = []
                data[t].append(0)
    sums.append(sum)

oak =  data['Quercus']
tsuga = data['Tsuga']

##gather pine together
pinus = []
pine1 = data['Pinus undiff.']
pine2 = data['Pinus subg. Strobus']
pine3 = data['Pinus subg. Pinus']
i = 0
while i < len(pine1):
    pval = pine1[i] + pine2[i] + pine3[i]
    pinus.append(pval)
    i +=1

##calculate pollen sum
i = 0
sums = []
while i < len(oak):
    thisSum = 0
    for item in data:
        if 'Lycopodium' not in item:
            try:
                thisSum += data[item][i]
                print thisSum
            except Exception as e:
                print str(e)
    sums.append(thisSum)
    i += 1

div1x = [0, 400]
div1y = [6300, 6300]
div2x = [0, 400]
div2y = [4900, 4900]

plt.plot(pinus, years, lw=0.5, label="Pinus (all)")
plt.plot(oak, years, lw=0.5, label="Quercus")
plt.plot(tsuga, years, lw=0.5, label="Tsuga")
plt.plot(div1x, div1y, lw=1, c='grey' )
plt.plot(div2x, div2y, lw=1, c='grey')
plt.legend()
plt.title("Tower Lake, Minnesota")
plt.xlabel("Raw Count")
plt.ylabel("Age (Radiocarbon BP)")
plt.show()

