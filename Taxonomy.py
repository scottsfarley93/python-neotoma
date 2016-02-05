__author__ = 'scottsfarley'

import sys
import urllib2
import json
#taxonName = sys.argv[1] ##

taxonName = ""
out = open("/Users/scottsfarley/documents/designChallenge/species.csv", 'w')
out.write("Name, NumSites\n")

nameEncoded = taxonName.replace(" ", "%20")

class taxonCollection:
    def __init__(self):
        self.items = []
    def __print__(self):
        return None

class Taxon:
    def __init__(self, sciName = ""):
        self.species = ""
        self.genus = ""
        self.family = ""
        self.order = ""
        self.taxonClass = "" ##conflicts with namespace
        self.phylum = ""
        self.numSites = 0
        self.sciName = sciName
    def __print__(self):
        return None


taxaEndpoint = "http://api.neotomadb.org/v1/data/taxa?"#taxonname=%" + nameEncoded + "%"
idEndpoint = "http://api.neotomadb.org/v1/data/taxa?taxonids="
siteEndpoint = "http://api.neotomadb.org/v1/data/datasets?taxonids="
print taxaEndpoint
results = urllib2.urlopen(taxaEndpoint)
response = json.load(results)
if response['success']:
    data = response['data']
    print "Found " + str(len(data)) + " taxa matching your query."
    for item in data:
        try:
            n = item['TaxonName']
            taxonId = item['TaxonID']
            apiString = siteEndpoint + str(taxonId)
            r = urllib2.urlopen(apiString)
            sitesResults = json.load(r)
            sitesData = sitesResults['data']
            numSites = len(sitesData)
            s = item['TaxonName'] + "," + str(numSites) + "\n"
            print s
            out.write(s)
        except:
            pass

        # currentID = 0
        # higherIDs = []
        # higherNames = []
        # i = 1
        # while str(currentID) != str(taxonId):
        #     if i != 1:
        #         taxaAPIString = idEndpoint + str(currentID)
        #     else:
        #         taxaAPIString = idEndpoint + str(taxonName)
        #     response = urllib2.urlopen(taxaAPIString)
        #     idResults = json.load(response)
        #     idData = idResults['data']
        #     currentID = idData['HigherTaxonID']
        #     higherIDs.append(currentID)
        #     higherNames.append(idData['TaxonName'])
        #     print idData['TaxonName']
        # print higherNames


