__author__ = 'scottsfarley'
import os
import csv

fileName = "/Users/scottsfarley/documents/designChallenge/Lookup.csv"
with open(fileName, 'rU') as lookupFile:
    csvReader = csv.DictReader(lookupFile)
    for row in csvReader:
        sciName = row['ScientificName']
        if row['Done?'] != "Y" or row['Done'] != "y":
            command = "python speciesToShapefile.py '" + str(sciName) + "'"
            print command
            os.system(command)