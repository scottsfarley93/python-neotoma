##todo:
##2.  Load taxa/ecol group values from lookup table
##3.  Accept both lists/tuples and integers in getDatasetDownload --> implement new class: Dataset Collection



from classes import * ##This file has all of the class definitions necessary for the api responses
import urllib2
import json


def stripDigits(s):
    """Removes numeric characters"""
    import re
    return re.sub("\d+", "", s)




########CONTACTS#################
def getContact(contactid = "", contactname = "", contactstatus = "", familyname = "", **kwargs):
    """Gets contacts from the neotoma database api.
        Parameters:
            Contact ID: A valid neotoma contactID of type integer
            Contact Name: A full or partial name to search for.  Numbers will be removed, but the string can contain
                search characters [%, *].  See the API documentation for details.
            Contact Status: The status of the contact you are searching for.
                Valid options are: ["ACTIVE", 'DECEASED', "DEFUNCT", "EXTANT", "INACTIVE", "RETIRED", "UNKNOWN"]
            Family Name:  The last name / family name of the contact you are searching for.
        Returns:
            ContactCollection
    """
    endpoint = "http://api.neotomadb.org/v1/data/contacts"
    url = endpoint  + "?"
    if contactid != "":
        try:
            contactid = int(contactid)
        except ValueError:
            print "Invalid contactID input."
            return False
        url += "contactid=" + str(contactid) + "&"
    if contactname != "":
        try:
            contactname = stripDigits(contactname)
            contactname = str(contactname)
        except:
            print "Invalid contact name input."
            return False
        url += "contactname=" + str(contactname) + "&"
    if contactstatus != "":
        try:
            contactstatus = str(contactstatus)
        except:
            print "Invalid contact status input."
            return False
        if contactstatus.upper() not in ["ACTIVE", 'DECEASED', "DEFUNCT", "EXTANT", "INACTIVE", "RETIRED", "UNKNOWN"]:
            print "Invalid contact status input."
            return False
        url += "contactstatus=" + contactstatus + "&"
    if familyname != "":
        try:
            familyname = stripDigits(familyname)
            familyname = str(familyname)
        except:
            print "Invalid Family Name input."
            return False
        url += "familyname=" + familyname + "&"
    CC = ContactCollection()
    if url[-1] == "&":
        url = url[:-1]
    print url
    response = urllib2.urlopen(url)
    data = json.load(response)
    success = data['success']
    if success != 1:
        print "Failed to obtain contacts."
        print data['message']
        return False
    else:
        contactData = data['data']
        i = 0
        while i < len(contactData):
            con = contactData[i]
            conID = con['ContactID']
            conAliasID = con['AliasID']
            conName = con['ContactName']
            conStatus = con['ContactStatus']
            conFamilyName = con['FamilyName']
            conLeadingInitials = con['LeadingInitials']
            conGivenNames = con['GivenNames']
            conSuffix = con['Suffix']
            conTitle = con['Title']
            conPhone = con['Phone']
            conFax = con['Fax']
            conEmail = con['Email']
            conURL = con['URL']
            conAddress = con['Address']
            conNotes = con['Notes']
            C = Contact(contactID=conID, aliasID=conAliasID, contactName=conName, contactStatus=conStatus, familyName=conFamilyName,
                        leadingInitials=conLeadingInitials, givenNames=conGivenNames, suffix=conSuffix, title=conTitle,
                        phone=conPhone, fax=conFax, email=conEmail, url=conURL, address=conAddress, notes=conNotes)
            CC.addContact(C)
            i +=1
        print "Found " + str(len(CC.items)) + " and returned them as a ContactCollection."
        return CC

##########PUBLICATIONS##############
"""
Legacy	Legacy citation ingested from another database and not parsed into separate fields
Journal Article	Article in a journal
Book Chapter	Chapter or section in an edited book
Authored Book	An authored book
Edited Book	An edited book
Master's Thesis	A Master's thesis
Doctoral Dissertation	A doctoral dissertation or Ph.D. thesis
Authored Report	An authored report
Edited Report	An edited report
Other Authored	An authored publication not fitting in any other category (e.g. web sites, maps)
Other Edited	An edited publication not fitting into any other category
"""

def getPublication(pubid="", contactid = "", datasetid = "", author = "", pubtype ="", year = "", search = "", **kwargs):
    """Get publications from the neotoma database.
        Parameters:
            pubid: A valid unique publication id in the neotoma database
            contactid: A valid unique contact id in the neotoma database
            datasetid: A valid unique dataset identified in the neotoma database
            author: A search string of characters for the author of a publication
            year: year publication was written
            search: A term to search the publication citation for
        Output:
            PublicationCollection Object
    """
    endpoint = "http://api.neotomadb.org/v1/data/publications"
    url = endpoint + "?"
    if pubid != "":
        try:
            pubid = int(pubid)
        except:
            print "Invalid publication id input."
            return False
        url += "pubid=" + str(pubid) + "&"
    if contactid != "":
        try:
            contactid = int(contactid)
        except:
            print "Invalid contact id."
            return False
        url += "contactid=" + str(contactid) + "&"
    if datasetid != "":
        try:
            datasetid = int(datasetid)
        except:
            print "Invalid dataset id input."
            return False
        url += "datasetid=" + str(datasetid) + "&"
    if author != "":
        try:
            author = str(author)
            author = stripDigits(author)
        except:
            print "Invalid author input."
            return False
        url += "author=" + author + "&"
    if pubtype != "":
        pubtypes = ["Legacy", "Journal Article", "Book Chapter", "Authored Book", "Edited Book", "Master's Thesis", "Doctorial Dissertation",
                    "Authored Report", "Edited Report", "Other Authored", "Other Edited"]
        try:
            pubtype = str(pubtype)
            if pubtype not in pubtypes:
                print "Invalid publication type input."
                print "Type must be one of:"
                print pubtypes
                return False
        except:
            print "Invalid publication type input."
            return False
        url += "pubtype=" + pubtype + "&"
    if year != "":
        try:
            year = int(year)
        except:
            print "Invalid year input."
            return False
        url += "year=" + year + "&"
    if search != "":
        url += "search=" + search
    PC = PublicationCollection()
    if url[-1] == "&":
        url = url[:-1]
    response = urllib2.urlopen(url)
    data = json.load(response)
    success = data['success']
    if success != 1:
        print "Failed to obtain publication collection."
        print data['message']
        return False
    else:
        i = 0
        pubData = data['data']
        while i < len(pubData):
            pub = pubData[i]
            pubID = pub['PublicationID']
            pubType = pub['PubType']
            pubYear = pub['Year']
            pubCitation = pub['Citation']
            pubAuthors = pub['Authors']
            P = Publication(id=pubID, type=pubType, year=pubYear, citation=pubCitation)
            j = 0
            while j < len(pubAuthors):
                auth = pubAuthors[j]
                cID = auth['ContactID']
                cName = auth['ContactName']
                order = auth['Order']
                A = Author(contactID=cID, contactName=cName, order=order)
                P.addAuthor(A)
                j +=1
            PC.addItem(P)
            i +=1
        print "Found " + str(len(PC.items)) + " and returned them as a PublicationCollection."
        return PC

#######SITES##############


def getSite(sitename="", altmin=-1, altmax=-1, loc=(), gpid=0, getCollectionUnits=False, **kwargs):
    """Query the neotoma database for research sites
        Parameters:
            sitename: A search string for the name of the research site
            altmin: An integer representing the minimum altitude of sites in the query return
            altmax An integer representing the maximum altitude of the sites in the query return
            loc: A tuple or list of the bounding box for which to search in format: [longW, latS, longE, latN]
            gpid= integer representing the geopolitical id number in which to query sites
            getCollectionUnits = boolean to determine if the return includes the collections units at the site
                True: return colllection units
                False: return only site metadata
        Return:
            SiteCollection
    """
    SC = siteCollection(sitename=sitename, altmin=altmin, altmax=altmax, loc=loc,
                        gpid=gpid, getCollectionUnits = getCollectionUnits)
    endpoint = "http://api.neotomadb.org/v1/data/sites"
    url = endpoint + "?"
    ##Build api query
    if sitename != "": ##name of site
        try:
            sitename = str(sitename)
        except:
            print "Invalid sitename input."
            return False
        url += "sitename=" + sitename
    if altmin != -1: ##minimum altitude
        try:
            altmin = float(altmin)
        except:
            print "Invalid altmin input."
            return False
        url += "&altmin=" + str(altmin)
    if altmax != -1:##maximum altitude
        try:
            altmax = float(altmax)
        except:
            print "Invalid altmax input."
            return False
        url += "&altmax=" + str(altmax)
    if loc != (): ##location bounding box
        try:
            assert isinstance(loc, tuple) or isinstance(loc, list)
            assert len(loc) == 4
            for i in loc:
                assert str(i).isdigit()
        except AssertionError:
            print "Invalid location bounding box."
            return False
        url = "&loc=" + str(loc[0]) + "," + str(loc[1]) + "," + str(loc[2]) + "," + str(loc[3])
    if gpid != 0:
        ##todo: validate this
        try:
            gpid = str(gpid)
            if gpid.isdigit():
                gpid = int(gpid)
            else:
                gpid = int(lookupGPID(keyword=gpid))
        except:
            print "Invalid gipd input."
            return False
        url += "&gpid=" + str(gpid)
    if url[-1] == "&":
        url = url[:-1]
    response = urllib2.urlopen(url)
    data = json.load(response)
    success = data['success']
    if success != 1:
        print "Failed to obtain valid sites response:"
        message = data['message']
        print message
        return False
    else:
        responseData = data['data']
        ##iterate through the returned sites and create objects for them
        i = 0
        while i < len(responseData):
            site = responseData[i]
            ##make a new Site object and populate it
            siteID = site['SiteID']
            ##we don't have collections from this call
            ##get individual site properties to get the collections unit field
            ##but only if we need this extra data
            if getCollectionUnits:
                S = getSiteByID(siteID) ##this will return the whole site object, will collections unit field
            else:
                ##do the object creation here and don't get collections unit
                sitename = site['SiteName']
                longE = site['LongitudeEast']
                longW = site['LongitudeWest']
                latN = site['LatitudeNorth']
                latS = site['LatitudeSouth']
                siteDesc = site['SiteDescription']
                S = Site(siteID = siteID, siteName=sitename, longE=longE, longW=longW, latN=latN, latS=latS, desc=siteDesc)
            SC.addSiteToCollection(S)
            i +=1
        print "Found " + str(len(SC.items)) + " sites and returned them as a SiteCollection."
        return SC ##return the site collection object

def getSiteByID(siteID):
    """Query the neotoma database for a specific siteID.
        Parameters:
            siteID: An integer representing a unique dataset identifier in the neotoma database.
        Returns:
            object of class Site
    """
    endpoint = "http://api.neotomadb.org/v1/data/sites/"
    url = endpoint + str(siteID)
    if url[-1] =="&":
        url = url[:-1]
    response = urllib2.urlopen(url)
    data = json.load(response)
    success = data['success']
    if success != 1:
        print "Failed to load valid site details:"
        print data['message']
        return False
    else:
        responseData = data['data']
        i = 0
        while i < len(responseData): ##there should only be one object from this call
            item = responseData[i]
            print item
            sitename = item['SiteName']
            longE = item['LongitudeEast']
            longW = item['LongitudeWest']
            latN = item['LatitudeNorth']
            latS = item['LatitudeSouth']
            siteDesc = item['SiteDescription']
            siteID = item['SiteID']
            collectionUnits = item['CollectionUnits']
            ##make a new site object an populate its attributes
            S = Site(siteName=sitename, siteID=siteID, longW=longW, longE=longE, latN=latN, latS=latS, desc = siteDesc)
            j = 0
            while j < len(collectionUnits):
                ##iterate through all collection unts
                unit = collectionUnits[j]
                unitID = unit['CollectionUnitID']
                unitHandle = unit['Handle']
                unitType = unit['CollType']
                ##make a new Collection Unit
                CU = CollectionUnit(cuID=unitID, handle=unitHandle, collType=unitType)
                ##add datasets to the datasets attribute
                unitDatasets = unit['Datasets']
                q = 0
                while q < len(unitDatasets):
                    dset = unitDatasets[q]
                    dtype = dset['DatasetType']
                    dID = dset['DatasetID']
                    ##make a new Dataset objet
                    D = DatasetDescription(datasetType=dtype, datasetID=dID)
                    ##add the dataset to the collection unit
                    CU.addDatasetToCollection(D)
                    q +=1
                S.addCollection(CU)
                j +=1
            i +=1
        return S


#############TAXA#################
"""
AVE	Birds
BIM	Biometric variables
BRY	Bryophytes
BTL	Beetles
FSH	Fish
HRP	Reptiles and amphibians
LAB	Laboratory analyses
MAM	Mammals
MOL	Molluscs
PHY	Physical variables
TES	Testate amoebae
VPL	Vascular plants
"""

def getTaxa(taxonID ="", taxonName = "", status = "", taxagroup = "", ecolGroup = "", **kwargs):
    """Query the neotoma database for taxa
        Parameters:
            taxonid: integer representing unique taxa id in the neotoma database
            taxonname: a string representing the full or partial name of the taxon
            status: a string that is one of: ['Extant", "Extinct", or "all].  Default is all
            taxagroup: a string representing the group in which the taxa is categorized
            ecolGroup: a string representing the ecological group in which the taxa is categorized
        Returns:
            TaxaCollection
    """
    taxonCodes = ["AVE", "BIM", "BRY", "BTL", "FSH", "HRP", "LAB", "MAM", "MOL", "PHY", "TES", "VPL"]
    taxonCodeLookup = ["Birds", "Biometric Variables", "Bryophytes", "Beetles", "Fish", "Reptiles and amphibians",
                       "Laboratory analysis", "Mammals", "Mollusks", "Physical variables", "Testate amoebae", "Vascular plants"]
    endpoint = "http://api.neotomadb.org/v1/data/taxa"
    url = endpoint + "?"
    if taxonID != "":
        try:
            taxonID = int(taxonID)
        except ValueError:
            print "Invalid taxon ID input."
            return False
        url  += "taxonID=" + str(taxonID) + "&"
    if taxonName != "":
        try:
            taxonName= stripDigits(taxonName)
            taxonName = str(taxonName)
        except:
            print "Invalid contact name input."
            return False
        taxonName = taxonName.replace(" ", "%20") ##url encode
        url += "taxonName=" + taxonName + "&"
    if status != "":
        try:
            status = str(status)
            if status.upper() not in ['EXTINCT', "EXTANT", "ALL"]:
                raise ValueError
        except:
            print "Invalid status input."
            return False
        url += "status=" + status + "&"
    if taxagroup != "":
        try:
            taxagroup = str(taxagroup)
            if taxagroup.upper() in taxonCodes: ##check if it is in code form
                pass
            elif taxagroup in taxonCodeLookup:
                    index = taxonCodeLookup.index(taxagroup)
                    taxagroup = taxonCodes[index]
            else:
                raise ValueError
        except:
            print "Invalid taxa group."
            return False
        url += "taxagroup=" + taxagroup + "&"
    if ecolGroup != "":
        ##todo: validate this
        try:
            ecolGroup = str(ecolGroup)
        except:
            print "Invalid ecological group."
            return False
        url += "ecolgroup=" + ecolGroup
    ##do the api call
    if url[-1] == "&":
        url = url[:-1]
    response = urllib2.urlopen(url)
    data = json.load(response)
    success = data['success']
    if success != 1:
        print "Failed to obtain taxon records:"
        print data['message']
        return False
    else:
        taxonData = data['data']
        collection = TaxaCollection()
        ##add returned results to the taxa collection
        i = 0
        while i < len(taxonData):
            t = taxonData[i]
            tID = t['TaxonID']
            tCode = t['TaxonCode']
            tName = t['TaxonName']
            tAuthor = t['Author']
            tExtinct = t['Extinct']
            tTaxaGroup = t['TaxaGroupID']
            tEcolGroup = t['EcolGroups']
            tHigherID = t['HigherTaxonID']
            tPubID = t['PublicationID']
            tNotes = t['Notes']
            T = Taxon(taxonID = tID, taxonCode=tCode, taxonName= tName, author=tAuthor, extinct=tExtinct, taxaGroup=tTaxaGroup,
                      ecolGroup=tEcolGroup, higherTaxonID=tHigherID, publicationID=tPubID, notes=tNotes)
            collection.addTaxon(T)
            i +=1
        print "Found " + str(len(collection.items)) + " taxa and returned them as a TaxaCollection."
        return collection

##########SampleData###########
##todo: validate this
def getSampleData(taxonids = "", taxonname = "", ageold= "", ageyoung = "", loc= (), gpid = "", altmin = "", altmax = "", **kwargs):
    """Query the neotoma database for raw sample data
        Parameters:
            taxonids: A list or tuple of integers or a single integer representing one or more taxon identifier to search for
            taxonname: A list or tuple of strings or a single string representing one or more full or partial names to search for
            ageold: An integer that represents the limit for the oldest data to be returned
            ageyoung: An integer that represents the limit for the youngest data to be return
            gpid: An integer representing a valid geopolitical unit in the neotoma database in which to limit query results
            altmin: An integer representing the lowest altitude data to be returned
            altmax: An integer representing the highest altitude data to be returned
        Returns:
            SampleDataCollection
    """
    endpoint = "http://api.neotomadb.org/v1/data/sampledata"
    url = endpoint  + "?"
    if taxonids != "":
        idList = ""
        if isinstance(taxonids, list):
            for i in taxonids:
                idList += i.replace(" ", "%20") + ","
        elif isinstance(taxonids, str):
            idList = taxonids.replace(" ", "%20")
        url += "taxonids=" + idList + "&"
    if taxonname != "":
        nameList = ""
        if isinstance(taxonname, list):
            for i in taxonname:
                nameList += i + ","
        elif isinstance(taxonname, str):
            nameList = taxonname.replace(" ", "%20")
        url += "taxonname=" + nameList + "&"
    if ageold != "":
        url += "ageold="  + ageold + "&"
    if ageyoung != "":
        url += "ageyoung=" + ageyoung + "&"
    if loc != ():
        locString = ""
        if not isinstance(loc, tuple) or not isinstance(loc, list):
            print "Location bounding box must be a list or a tuple."
            return False
        for i in loc:
            locString += str(i) + ","
        url += "loc=" + locString + "&"
    if gpid != "":
        gpid = str(gpid)
        if gpid.isdigit():
            gpid = int(gpid)
        else:
            gpid = int(lookupGPID(keyword=gpid))
    if altmin!= "":
        url += "altmin=" + altmin
    if altmax != "":
        url += "altmax=" + altmax

    SC = SampleDataCollection()
    if url[-1] == "&":
        url = url[:-1]
    response = urllib2.urlopen(url)
    data = json.load(response)
    success = data['success']
    if success != 1:
        print "Failed to obtain sample data."
        print data['message']
        return False
    else:
        responseData = data['data']
        i = 0
        while i < len(responseData):
            d = responseData[i]
            dTaxaGroup = d['TaxaGroup']
            dValue = d['Value']
            dUnits = d['VariableUnits']
            dTaxonName = d['TaxonName']
            dElement = d['VaraibleElement']
            dContext = d['VariableContext']
            dSampleAge = d['SampleAge']
            dAgeYounger = d['SampleAgeYounger']
            dAgeOlder = d['SampleAgeOlder']
            dDatasetID = d['DatasetID']
            dSiteAltitude = d['SiteAltitude']
            dLatN = d['SiteLatitudeNorth']
            dLatS = d['SiteLatitudeSouth']
            dLongE = d['SiteLongitudeEast']
            dLongW = d['SiteLongitudeWest']
            SD = SampleData(taxagroup=dTaxaGroup, value=dValue, variableUnits=dUnits, taxonName=dTaxonName, variableElement=dElement,
                            variableContext=dContext, sampleAge=dSampleAge, sampleAgeYounger=dAgeYounger, sampleAgeOlder=dAgeOlder,
                            datasetID=dDatasetID, siteAltitude=dSiteAltitude, siteLatitudeN=dLatN, siteLatitudeS=dLatS,
                            siteLongitudeE=dLongE, siteLongitudeW=dLongW)
            SC.addSample(SD)
            i += 1
        print "Found " + str(len(SC.items)) + " sites and returned them as a SampleCollection."
        return SC

def downloadDataset(datasetID):
    """Download a single dataset
        Parameters:
            DatasetID: An integer representing a valid dataset identifier in the neotoma database
        Returns:
            object of type DatasetDownload
    """
    endpoint = "http://api.neotomadb.org/v1/data/downloads/"
    try:
        int(datasetID)
    except ValueError:
        print "Invalid datasetID format."
        return False
    url = endpoint + str(datasetID)
    response = urllib2.urlopen(url)
    data = json.load(response)
    success = data['success']
    if success != 1:
        print "Failed to download dataset."
        print data['message']
        return False
    else:
        for i in data['data']:
            datasetID = i['DatasetID']
            datasetName = i['DatasetName']
            unitHandle = i['CollUnitHandle']
            unitType = i['CollUnitType']
            datasetType = i['DatasetType']
            lastSub = i['NeotomaLastSub']
            chronID = i['DefChronologyID']
            PIs = i['DatasetPIs']
            site = i['Site']
            samples = i['Samples']
            download = DatasetDownload(datasetID=datasetID, datasetName=datasetName, collUnitHandle=unitHandle,
                                       collUnitType=unitType, datasetType=datasetType, neotomaLastSub=lastSub,
                                       defChronID=chronID)
            ##Add PIs
            i = 0
            while i < len(PIs):
                p = PIs[i]
                pid = p['ContactID']
                pName = p['ContactName']
                PI = datasetPI(id=pid, name=pName)
                download.addPI(PI)
                i +=1
            ##populate the site
            siteID = site['SiteID']
            siteName = site['SiteName']
            siteAlt = site['Altitude']
            siteLatN = site['LatitudeNorth']
            siteLatS = site['LatitudeSouth']
            siteLongE = site['LongitudeEast']
            siteLongW = site['LongitudeWest']
            siteDescription = site['SiteDescription']
            siteNotes = site['SiteNotes']
            downloadSite = Site(siteID=siteID, siteName=siteName, altitude=siteAlt, latN=siteLatN, latS=siteLatS,
                                longE=siteLongE, longW=siteLongW, desc=siteDescription)
            download.site = downloadSite

            ##populate the samples
            i = 0
            while i < len(samples):
                s = samples[i]
                sid = s['SampleID']
                sName = s['SampleName']
                sUnitName = s['AnalysisUnitName']
                sUnitDepth = s['AnalysisUnitDepth']
                sUnitThickness = s['AnalysisUnitThickness']
                sAges = s['SampleAges']
                sData = s['SampleData']
                S = Sample(sampleID=sid, sampleName=sName, unitName=sUnitName, unitDepth=sUnitDepth, unitThickness=sUnitThickness)
                j = 0
                while j < len(sAges):
                    a = sAges[j]
                    aid = a['ChronologyID']
                    aName = a['ChronologyName']
                    aType = a['AgeType']
                    aAge = a['Age']
                    aAgeYounger = a['AgeYounger']
                    aAgeOlder = a['AgeOlder']
                    Age = SampleAge(chronID=aid, chronName=aName, ageType=aType, age=aAge, ageYounger=aAgeYounger, ageOlder=aAgeOlder)
                    S.addAge(Age)
                    j +=1
                ##reset
                j = 0
                ##add sample data
                while j < len(sData):
                    d = sData[j]
                    dGroup = d['TaxaGroup']
                    dValue = d['Value']
                    dUnits = d['VariableUnits']
                    dName = d['TaxonName']
                    dElement = d['VariableElement']
                    dContext = d['VariableContext']
                    SD = SampleData(taxagroup=dGroup, value=dValue, variableUnits=dUnits, taxonName=dName, variableElement=dElement,
                                    variableContext=dContext)
                    S.addSampleData(SD)
                    j +=1
                download.addSample(S)
                i += 1
            return download


def getDatasetDownload(dids):
    """Query the neotoma database for multiple datasets and download their contents
        Parameters:
            dids: A list or tuple of integers or a single integer representing a the dataset identifiers to be downloaded
        Returns:
            DatasetCollection
    """
    datasetCollection = DatasetCollection()
    if isinstance(dids, list) or isinstance(dids, tuple):
        i = 0
        ##iterate through all ids in a list, append the dataset download, and return as a dataset collection
        while i < len(dids):
            thisID = dids[i]
            datasetDownload = downloadDataset(thisID)
            if not datasetDownload:
                return False ##invalid input
            else:
                datasetCollection.addItem(datasetDownload)
            i +=1
        return datasetCollection
    else:
        ##not a list or tuple --> go straight to download function
        datasetDownload = downloadDataset(dids)
        if not datasetDownload:
            return False
        else:
            datasetCollection.addItem(datasetDownload)
            return datasetCollection



##DATASETS
##Todo: Better valdiation on this method
def getDataset(siteid="", datasettype="", piid="", altmin="", altmax = "", loc=(), gpid="", taxonids="", taxonname="", ageold="",
                ageyoung="", ageof="", subdate="", **kwargs):

    """Query the neotoma database for datasets
        Parameters:
            siteid: an integer representing a site id number in neotoma database
            datasettype: A string representing a valid dataset type
            piid: An integer representing the unique id of the project PI for the site
            altmin: An integer representing the lowest altitude data to return
            altmax: An integer representing the highest altitude data to return
            loc: A list or tuple representing the bounding box of the data to be returned (longW, latS, longE, latN)
            gpid: An integer representing the geopolitical id in which to search for data
            taxonids: A list or tuple of integers or a single integer that represents the taxa id(s) for which to search
            taxaonname: A list or tuple of strings or a single string representing a full or partial taxon name for which to search
            ageold: An integer representing the oldest age data to be returned
            ageyoung: An integer representing the youngest age data to be returned
            ageof: A string
            subdata: A string of format YYYY-MM-DD or MM-DD-YYYY to represent the submission date of the dataset
        Returns:
            DatasetCollection
    """
    endpoint ="http://api.neotomadb.org/v1/data/datasets"
    url = endpoint + "?"
    if siteid != "":
        try:
            siteid = stripDigits(siteid)
            siteid = int(siteid)
        except:
            print "Invalid site id input"
            return False
        url += "siteid=" + str(siteid) + "&"
    if datasettype != "":
        ##validate input
        try:
            assert isinstance(datasettype, str)
        except:
            print "Dataset type invalid."
            return False
        datasettype = datasettype.replace(" ", "%20")
        if datasettype not in ["geochronologic", "loss-on-ignition", "pollen", "plant%20macrofossils", "vertegrate%20fauna",
                               "mollusks", "pollen%20surface%20sample"]:
            print "Dataset type not valid."
            return False
        url += "datasettype=" + str(datasettype) + "&"
    if piid != "":
        try:
            piid = int(piid)
        except:
            print "Invalid PIID input."
            return False
        url += "piid=" + str(piid) + "&"
    if altmin!= "":
        try:
            altmin = int(altmin)
        except :
            print "Invalid altitude minimum input."
            return False
        url += "altmin=" + str(altmin) + "&"
    if altmax != "":
        try:
            altmax = int(altmax)
        except:
            print "Invalid maximum altitude input."
            return False
        url += "altmax=" + str(altmax) + "&"
    if loc != ():
        ##make sure it is a list or tuple of length 4
        try:
            assert isinstance(loc, tuple) or isinstance(loc, list)
            assert len(loc) == 4
            ##and that all elements are numbers
            for i in loc:
                float(i)
        except (AssertionError, ValueError):
            print "Location bounding box input invalid."
            return False
        locString = ""
        for i in loc:
            locString += str(i) + ","
        url += "loc=" + locString + "&"
        ageof = "taxon"
    if gpid != "":
        ##todo: validate gpid
        gpid = str(gpid)
        if gpid.isdigit():
            gpid = int(gpid)
        else:
            gpid = int(lookupGPID(keyword=gpid))
        url += "gpid=" + str(gpid) + "&"
    if taxonids != "":
        try:
            assert isinstance(taxonids, list) or isinstance(taxonids, tuple)
            for i in taxonids:
                float(i)
        except:
            print "Invalid taxon id list."
            return False
        idList = ""
        for i in taxonids:
            idList += str(i) + ","
        url += "taxonids=" + idList
    if taxonname != "":
        taxonname = str(taxonname)
        url += "taxonname=" + taxonname.replace(" ", "%20") + "&"
        ageof = "taxon"
    if ageold != "":
        try:
            ageold = float(ageold)
        except:
            print "Old age input not valid."
            return False
        url += "ageold=" + str(ageold) + "&"
    if ageyoung != "":
        try:
            ageyoung = float(ageyoung)
        except:
            print "Young age input not valid."
            return False
        url += "ageyoung=" + str(ageyoung) + '&'
    if ageof != "":
        #validate
        if ageof.strip() not in ["sample", "taxon", "dataset"]:
            print "Ageof parameter not valid."
            return False
        url += "ageof=" + ageof + "&"
    if subdate != "":
        ##todo: validate submission date format
        url += "subdate=" + str(subdate) + "&"
    if url[-1] == "&":
        url = url[:-1]
    print url
    response = urllib2.urlopen(url)
    data= json.load(response)
    success = data['success']
    DC = DatasetCollection()
    if success != 1:
        print "Failed to obtain dataset."
        print data['message']
        return False
    else:
        for i in data['data']:
            did = i['DatasetID']
            dname = i['DatasetName']
            dUnitHandle = i['CollUnitHandle']
            dUnitID = i['CollectionUnitID']
            dUnitType = i['CollUnitType']
            dType = i['DatasetType']
            dAgeOldest = i['AgeOldest']
            dAgeYoungest = i['AgeYoungest']
            dSubDates = i['SubDates']
            dPIs = i['DatasetPIs']
            site = i['Site']

            D = Dataset(datasetID=did, datasetName=dname, colUnitHandle=dUnitHandle, colUnitID=dUnitID, colUnitType=dUnitType,
                        datasetType=dType, ageOldest=dAgeOldest, ageYoungest=dAgeYoungest)
            ##populate the site
            siteID = site['SiteID']
            siteName = site['SiteName']
            siteAlt = site['Altitude']
            siteLatN = site['LatitudeNorth']
            siteLatS = site['LatitudeSouth']
            siteLongE = site['LongitudeEast']
            siteLongW = site['LongitudeWest']
            siteDescription = site['SiteDescription']
            siteNotes = site['SiteNotes']
            datasetSite = Site(siteID=siteID, siteName=siteName, altitude=siteAlt, latN=siteLatN, latS=siteLatS,
                                longE=siteLongE, longW=siteLongW, desc=siteDescription)
            D.site = datasetSite

            ##populate the PIs
            for i in dPIs:
                cid = i['ContactID']
                cName = i["ContactName"]
                C = datasetPI(id=cid, name=cName)
                D.addPI(C)

            ##Populate the submission events
            for e in dSubDates:
                d = e['SubmissionDate']
                t = e['SubmissionType']
                Event = Submission(date=d, type=t)
                D.addSubEvent(Event)

            DC.addItem(D)
        print "Found " + str(len(DC.items)) + " datasets and returned them as a DatasetCollection."
        return DC



def getPINames(dataset):
    PI_List = dataset.datasetPIs
    returnList = []
    for person in PI_List:
        returnList.append(person.contactName)
    return returnList

def getCounts(dataset):
    import pandas as pd
    print dataset.__dict__
    samples = dataset.samples
    print samples
    header = []
    cursor =  0
    theMatrix = []
    depths = []
    ##first get all taxa that are used
    taxaSet = []
    for sample in samples:
        for item in sample.sampleData:
            taxaSet.append(item.taxonName)
    taxaSet = set(taxaSet)
    numTaxa = len(taxaSet)

    header = list(taxaSet) ##convert back to a list for the header
    for sample in samples:
        sampleDepth = sample.unitDepth
        depths.append(sampleDepth)
        unitThickness = sample.unitThickness
        sampleData = sample.sampleData
        unitTemplate = [0] * numTaxa
        for i in sampleData:
            taxonName = i.taxonName
            ##get the index
            index = header.index(taxonName)
            unitTemplate[index] = i.Value
        theMatrix.append(unitTemplate)
        cursor +=1
    theMatrix = pd.DataFrame(theMatrix, index=depths, columns=header)
    print theMatrix
    return theMatrix

def lookupGPID(keyword="", gpid=0):
    import urllib2
    endpoint = "http://api.neotomadb.org/v1/dbtables/GeoPoliticalUnits?limit=all"
    response = urllib2.urlopen(endpoint)
    data = json.load(response)
    success = data['success']
    if success != 1:
        print "Failed to get GPID lookup table."
        print "Message was: "
        print data['message']
        return False
    data = data['data']
    names = []
    codes = []
    for place in data:
        names.append(place['GeoPoliticalName'].upper())
        codes.append(place['GeoPoliticalID'])
    if keyword != "":
        index = names.index(keyword.upper())
        if index == -1:
            print "Invalid Geopolitical Unit input."
            return False
        else:
            code = codes[index]
            return code
    elif gpid != 0:
        index = codes.index(gpid)
        if index == -1:
            print "Invalid GPID input."
            return False
        else:
            name = names[index]
            return name


