__author__ = 'scottsfarley'
import API ##neotoma API wrapper
#import pandas
import csv
import sys

taxonName = sys.argv[1]
print "Running script for taxon: ", taxonName

datasetCollection = API.getDataset(taxonname=taxonName)
datasets = datasetCollection.items
DIDs = []
for dataset in datasets:
    did = dataset.datasetID
    DIDs.append(did) ##append each dataset's id to the list


theMatrix = []


row = {
    # "siteID": None,
    # "latN" :None,
    # "latS" :None,
    # "lngE" :None,
    # "lngW":None,
    # "siteName": None,
    # "taxaGroup" :None,
    # "taxonName" : None,
    # "value" :None,
    # "unitDepth" :None,
    # "minAge" :None,
    # "maxAge" :None,
    # "Age":None,
    # "element" :None,
    # "context" :None,
    # "variableUnits":None,
    # "submittedToDB":None,
    # 'altitude' :None,
    # 'datasetType' :None
}


output = []
output2 = []
counter = 0

downloadsCollection = API.getDatasetDownload(DIDs)
for item in downloadsCollection.items:
    subDate = item.neotomaLastSub
    dType = item.datasetType
    did = item.datasetID
    site = item.site
    siteID = site.siteID
    siteLatN = site.latN
    siteLatS = site.latS
    siteLngE = site.longE
    siteLngW = site.longW
    avgLat = (siteLatN + siteLatS) / 2
    avgLng = (siteLngW + siteLngE) / 2
    siteName = site.siteName
    siteAlt = site.alitutde
    for sample in item.samples:
        depth = sample.unitDepth
        sampleAge = sample.sampleAges[0]
        ageType = sampleAge.ageType
        age = sampleAge.age
        ageYounger = sampleAge.ageYounger
        ageOlder = sampleAge.ageOlder
        ##generate pollen sum
        if dType == "pollen":
            pollenSum = 0
            for sampleData in sample.sampleData:
                if sampleData.variableElement == "pollen":
                    pollenSum += sampleData.Value

        itemRow = {}
        for sampleData in sample.sampleData:
            try:
                checkName = str(sampleData.taxonName).upper()
            except:
                checkName = "" ## avoids unicode errors
            if checkName == taxonName.upper():
                itemRow['siteID'] = siteID
                itemRow['latN'] = siteLatN
                itemRow['latS'] = siteLatS
                itemRow['lngE'] = siteLngE
                itemRow['lngW'] = siteLngW
                itemRow['lat'] = avgLat
                itemRow['lng'] = avgLng
                itemRow['siteName'] = siteName
                itemRow['taxaGroup'] = sampleData.taxaGroup
                itemRow['taxonName'] = sampleData.taxonName
                itemRow['value'] = sampleData.Value
                itemRow['unitDepth'] = depth
                itemRow['minAge'] = ageYounger
                itemRow['maxAge'] = ageOlder
                itemRow['Age'] = age
                itemRow['ageType'] = ageType
                itemRow['element'] = sampleData.variableElement
                itemRow['context'] = sampleData.variableContext
                itemRow['variableUnits'] = sampleData.variableUnits
                itemRow['submittedToDB'] = subDate
                itemRow['altitude'] = siteAlt
                itemRow['datasetType'] = dType
                if dType == "pollen":
                    itemRow['pollenSum'] = pollenSum
                    itemRow['pollenPct'] = (sampleData.Value / pollenSum) * 100
                output.append(itemRow)




with open('/Users/scottsfarley/documents/designChallenge/CSVs/' + str(taxonName) + '.csv', 'w') as outfile:
    header = ['siteID', 'siteName', 'lat', 'lng', 'latN', 'latS', 'lngE', 'lngW', 'taxaGroup', 'taxonName', 'value', 'variableUnits', 'element','context', 'Age', 'minAge', 'maxAge', 'ageType', 'unitDepth', 'altitude', 'datasetType', 'submittedToDB', "pollenSum", "pollenPct"]
    writer = csv.DictWriter(outfile, header)
    writer.writeheader()
    i = 0
    while i < len(output):
        row = output[i]
        writer.writerow(row)
        i +=1
    outfile.close()
    print "All Done."








