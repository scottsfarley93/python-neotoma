import requests
import API
import csv

def recursiveNameFinder(name):
    search = []
    kingdomNames = ["archaea", "protista", "fungi", "animalia", "plantae"]
    queryName = str(name)
    queryName = queryName.replace(" ", "%20")
    endpoint = "http://api.neotomadb.org/v1/data/taxa?taxonname=" + queryName
    results = requests.get(endpoint).json()
    if results['success']:
        data = results['data']
        for i in data:
            name = ""
            startNodeName = i['TaxonName']
            higherID = i['HigherTaxonID']
            while name.lower() not in kingdomNames:
                idEndpoint = "http://api.neotomadb.org/v1/data/taxa?taxonid=" + str(higherID)
                idResponse = requests.get(idEndpoint).json()
                if idResponse['success']:
                    name = idResponse['data'][0]['TaxonName']
                    search.append(name)
                    higherID = idResponse['data'][0]['HigherTaxonID']
                else:
                    print "Failed."
                    break
            return search



#r = recursiveNameFinder("sequoia")



def commonNameFinder(name):
    tsns = []
    endpoint = "http://www.itis.gov/ITISWebService/jsonservice/ITISService/searchForAnyMatch?srchKey="
    name = str(name)
    name.replace(" ", "%20")
    apiString = endpoint + str(name)
    results = requests.get(apiString).json()
    matchList = results['anyMatchList']
    possibleCommonNames = []
    for item in matchList:
        tsn = int(item['tsn'])
        cnl = item['commonNameList']
        ##find which name to get hierarchy for
        itemSciName = item["sciName"]
        if "var." not in itemSciName:
            for n in cnl['commonNames']:
                ##decide if we should add the name to the list
                if n['language'] == "English":
                    commonName = n['commonName']
                    if commonName not in possibleCommonNames:
                        possibleCommonNames.append(commonName)
    return possibleCommonNames

def getTSN(name, i=0, minRank = 0):
    endpoint = "http://www.itis.gov/ITISWebService/jsonservice/ITISService/searchForAnyMatch?srchKey=" + str(name)
    results = requests.get(endpoint).json()
    print "Request to itis: OKAY"
    matchList = results['anyMatchList']
    if len(matchList) > 0:
        selected = matchList[i]
        tsn = selected['tsn']
        if minRank == 0:
            print "Print found ", len(matchList) , "options for ", name, " taking index #", i, " OKAY"
            return int(tsn)
        if minRank > 0:
            tSplit = selected['sciName'].split(" ")
            if len(tSplit) == 2:
                print "Did not meet valid rank criteria.  Trying again."
                getTSN(name, i=i+1)
            print "Print found ", len(matchList) , "options for ", name, " taking index #", i, " OKAY"
            return int(tsn)
    else:
        print "No matches found. "
        return None


# for item in r:
#     print item, commonNameFinder(item)



def siteFinder(name):
    name = str(name)
    name = name.replace(" ", "%20")
    endpoint = "http://api.neotomadb.org/v1/data/datasets?taxonname=" + name
    results = requests.get(endpoint).json()
    if results['success']:
        data = results['data']
        return len(data)

def getAllTaxa():
    endpoint = "http://api.neotomadb.org/v1/data/taxa?taxagroup=MAM"
    results = requests.get(endpoint).json()
    if results['success']:
        data = results['data']
        return data


def getSpeciesDataToCSV(tName, fName):
    print "Running getSpeciesDataToCSV: ", tName, fName
    datasetCollection = API.getDataset(taxonname=tName)
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


    downloadsCollection = []
    ##do one by one because batch takes too long to wait for response
    for download in DIDs:
        d = API.getDatasetDownload(download)
        print d
        for item in d.items:
            downloadsCollection.append(item)



    e = 0
    for item in downloadsCollection:
        e +=1
        print e
        try:
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
                print depth
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
                    if checkName == tName.upper():
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
                        print itemRow
        except:
            print "Passing."


        with open(fName, 'w') as outfile:
            print "File is open."
            header = ['siteID', 'siteName', 'lat', 'lng', 'latN', 'latS', 'lngE', 'lngW', 'taxaGroup', 'taxonName', 'value', 'variableUnits', 'element','context', 'Age', 'minAge', 'maxAge', 'ageType', 'unitDepth', 'altitude', 'datasetType', 'submittedToDB', "pollenSum", "pollenPct"]
            writer = csv.DictWriter(outfile, header)
            writer.writeheader()
            i = 0
            while i < len(output):
                row = output[i]
                writer.writerow(row)
                i +=1
            outfile.close()
            print "File is closed."
    print "Function has terminated."


# allTaxa = getAllTaxa()
#
#
# numCommonNames = []
# searchTerms = []
# numSites = []
# numParents = []
# taxonomies = []
# commonNames = []

# for tObj in allTaxa:
#     t = tObj['TaxonName']
#     n = siteFinder(t)
#     numSites.append(n)
#     searchTerms.append(t)
#     taxonomy = recursiveNameFinder(t)
#     taxonomies.append(taxonomy)
#     numParents.append(len(taxonomy))
#     cnames = commonNameFinder(t)
#     commonNames.append(cnames)
#     numCommonNames.append(len(cnames))
#     print "----"
#     print "Name: ", t
#     print "Common Names (", len(cnames), "): ", cnames
#     print "Sites: ", n
#     print "Num Parents: ", len(taxonomy)
#     print "Parents: ", taxonomy
#     print "Common Names Distribution: ", numCommonNames
#     print "Parents Distribution: ", numParents
#     print "Sites Distribution: ", numSites
#
# print "Number of common names: ", numCommonNames
# print "Number of common sites: ", numSites
# print "number of parents: ", numParents
def getTaxonomicRank(name, index=None):
    tsn = getTSN(name, index)
    if tsn is not None:
        endpoint = "http://www.itis.gov/ITISWebService/jsonservice/ITISService/getTaxonomicRankNameFromTSN?tsn=" + str(tsn)
        results = requests.get(endpoint).json()
        rank = results['rankName']
        print "Rank is", rank
        return rank
    else:
        print "TSN was none."
        return None

def taxonomyToDict(taxonomy):
    results = []
    index = 0
    for item in taxonomy:
        tRank = getTaxonomicRank(item, index=index)
        results.append(tRank)
        index += 1
    tDict= zip(results, taxonomy)
    print tDict
    return tDict

# a = recursiveNameFinder("bison bison")
# print taxonomyToDict(a)