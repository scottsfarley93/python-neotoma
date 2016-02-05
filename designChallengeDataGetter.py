__author__ = 'scottsfarley'
print "Started dataGetter."
import API
from scratch import recursiveNameFinder, commonNameFinder, siteFinder, getSpeciesDataToCSV
import requests
import json
import csv

##I/O control
commonLookup = "/Users/scottsfarley/documents/designChallenge/plants/common.csv"
hLookup = "/Users/scottsfarley/documents/designChallenge/plants/taxonomy.csv"
mainLookup = "/Users/scottsfarley/documents/designChallenge/plants/main.csv"
dataFolder = "/Users/scottsfarley/documents/designChallenge/plants/"
passFile = "/Users/scottsfarley/documents/designChallenge/plants/pass.csv"
displayFolder = "plants/"

commonLookupOpen = open(commonLookup, 'a+')
hLookupOpen = open(hLookup, 'a+')
mainLookupOpen = open(mainLookup, 'a+')
passOpen = open(passFile, 'a+')
passOpen.write("name,\n")

r = csv.DictReader(mainLookupOpen)
done = []
for row in r:
    d = row['Taxon Name']
    done.append(d)

passed = csv.DictReader(passOpen)
for row in passed:
    d = row['name']
    done.append(d)

mainHeaders = "Taxon Name, numOccurrences, fileName\n"
mainLookupOpen.write(mainHeaders)


def getTaxaInGroup(groupCode):
    g = []
    endpoint = "http://api.neotomadb.org/v1/data/taxa?taxagroup=" + str(groupCode)
    results = requests.get(endpoint).json()
    for i in results['data']:
        g.append(i['TaxonName'])
    return g

def getDataForList(taxonList, threshold = 10):
    for taxon in taxonList:
        tSplit = taxon.split(" ")
        if len(tSplit) == 2 and taxon not in done:
            ##check if there are more than threshold occurrences in neotoma
            print "Working on taxon: ", taxon
            n = siteFinder(taxon)
            if int(n) < int(threshold):
                print "Not enough occurrences. Passing."
                s = taxon + ",\n"
                passOpen.write(s)
            else:
                try:
                    ##enough records --> get the data
                    fileName = dataFolder + taxon + ".csv" ## this is where the occurrences will be listed
                    mainInsert = taxon + "," + str(n) + "," + displayFolder + taxon + ".csv" + ",\n"
                    mainLookupOpen.write(mainInsert)
                    print "Insert into main lookup: OKAY."
                    ##get common names
                    commons = commonNameFinder(taxon)
                    commonInsert = taxon + ","
                    for c in commons:
                        commonInsert += str(c) + ","
                    commonInsert += "\n"
                    commonLookupOpen.write(commonInsert)
                    print "Got " + str(len(commons)) + " common names: OKAY"
                    ## get sci hierarchy
                    h = recursiveNameFinder(taxon)
                    print h
                    taxonomyInsert = taxon + ","
                    i = len(h)
                    while i > 0:
                        taxonomyInsert += h[i-1] + ","
                        i -= 1
                    taxonomyInsert += "\n"
                    hLookupOpen.write(taxonomyInsert)
                    print "Got taxonomy of length ", str(len(h)) + ": OKAY"
                    ## get the actual data
                    getSpeciesDataToCSV(taxon, dataFolder + taxon + ".csv")
                    print "Got species data: OKAY."
                    ##okay we are done
                except:
                    pass
            print "---------------"
        else:
            print "I think this is not a species name: " + str(taxon) + " or it has already been completed."






l = getTaxaInGroup("VPL")
getDataForList(l)