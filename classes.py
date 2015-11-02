__author__ = 'scottsfarley'
class DatasetCollection():
    def __init__(self):
        self.items = []
    def addItem(self, d):
        try:
            assert (isinstance(d, Dataset) or isinstance(d, DatasetDownload) or isinstance(d, DatasetDescription))
            self.items.append(d)
        except:
            print "Failed to add to DatasetCollection.  Item must be of type Dataset."
            print "Got type: ", type(d)
            print d

class ContactCollection():
    def __init__(self):
        self.items = []
    def addContact(self, C):
        try:
            assert isinstance(C, Contact)
            self.items.append(C)
        except AssertionError:
            print "Failed to add item to ContactCollection. Item must be of type Contact."

class Contact():
    def __init__(self, contactID = '', aliasID = "", contactName = "", contactStatus = "", familyName = "",
                 leadingInitials = "", givenNames = "", suffix = "", title = "", phone = "", fax = "", email = "",
                 url = "", address = "", notes = ""):
        self.contactID = contactID
        self.aliasID = aliasID
        self.contactName = contactName
        self.contactStatus = contactStatus
        self.familyName = familyName
        self.leadingInitials = leadingInitials
        self.givenNames = givenNames
        self.suffix = suffix
        self.title = title
        self.phone =phone
        self.fax= fax
        self.email = email
        self.url = url
        self.address = address
        self.notes= notes


class Dataset():
    def __init__(self, datasetID = 0, datasetName = "", colUnitHandle = "", colUnitID = "",
                 colUnitType = "", datasetType = "", ageOldest = "", ageYoungest = "", site = ""):
        self.datasetID = datasetID
        self.datasetName = datasetName
        self.colUnitHandle = colUnitHandle
        self.colUnitID = colUnitID
        self.colUnitType = colUnitType
        self.datasetType = datasetType
        self.ageOldest = ageOldest
        self.ageYoungest = ageYoungest
        self.site = site
        self.PIs = []
        self.SubEvents = []

    def addSubEvent(self, e):
        try:
            assert isinstance(e, Submission)
            self.SubEvents.append(e)
        except AssertionError:
            print "Failed to add to dataset.  Item must be of type Submission."
    def addPI(self, p):
        try:
            assert isinstance(p, datasetPI)
            self.PIs.append(p)
        except AssertionError:
            print "Failed to add to dataset.  Item must be of type datasetPI."


class Submission():
    def __init__(self, date = "", type = ""):
        self.submissionType = type
        self.submissionDate = date


class datasetPI():
    def __init__(self, id = "", name = ""):
        self.contactID = id
        self.contactName = name

class PublicationCollection():
    def __init__(self):
        self.items = []

    def addItem(self, item):
        try:
            assert isinstance(item, Publication)
            self.items.append(item)
        except:
            print "Failed to add item to PublicationCollection.  Item must be of type Publication."


class Publication():
    def __init__(self, id="", type= "", year = 0, citation = ""):
        self.publicationID = id
        self.publicationType = type
        self.Year = year
        self.citation = citation
        self.authors = []
    def addAuthor(self, author):
        try:
            assert isinstance(author, Author)
            self.authors.append(Author)
        except:
            print "Failed to add to Publication object.  Item must be of type Author."

class Author():
    def __init__(self, contactID = "", contactName = "", order = 0):
        self.contactID = contactID
        self.contactName = contactName
        self.order = order


class siteCollection():
    """Holds the properties for a collection of sites, with attributes about the query used to obtain them"""
    def __init__(self, sitename = "", altmin = -1, altmax=-1, loc = (), gpid=0, getCollectionUnits = True):
        self.sitename = sitename
        self.altmin = altmin
        self.altmax = altmax
        self.loc = loc
        self.gpid = gpid
        self.getCollectionUnits = getCollectionUnits
        self.items = []
    def getItemByIndex(self, index):
        return self.items[index]
    def addSiteToCollection(self, site):
        try:
            assert isinstance(site, Site)
            self.items.append(site)
        except AssertionError:
            print "Failed to add to site collection. Item must be of type Site."


class Site():
    def __init__(self, siteID = "", siteName = "", altitude = "",
                 latN = "", latS = "", longE = "", longW = "", desc = ""):
        """Constructor for site object"""
        self.siteID = siteID
        self.siteName = siteName
        self.alitutde = altitude
        self.latN = latN
        self.latS = latS
        self.longE = longE
        self.longW = longW
        self.siteDescription = desc
        self.collectionUnits = []
    def addCollection(self, collection):
        try:
            assert isinstance(collection, CollectionUnit)
            self.collectionUnits.append(collection)
        except AssertionError:
            print "Failed to add to Site.  Item must be of type Collection Unit."

class CollectionUnit():
    """"Collection unit object that holds the datasets for a site"""
    def __init__(self, cuID = "", handle = "", collType = ""):
        self.collectionUnitID = cuID
        self.handle = handle
        self.collType = collType
        self.datasets = []
        return
    def addDatasetToCollection(self, dataset):
        try:
            assert isinstance(dataset, Dataset)
            self.datasets.append(dataset)
        except AssertionError:
            print "Failed to add to Collection Unit.  Item must be of type Dataset."


class DatasetDescription():
    """Holds a neotoma dataset object's properties"""
    def __init__(self, datasetID = "", datasetType = ""):
        self.datasetID = datasetID
        self.datasetType = datasetType
        return


class TaxaCollection(): ##basically just a list of taxa
    def __init__(self):
        self.items = []
    def addTaxon(self, taxon):
        try:
            assert isinstance(taxon, Taxon)
            self.items.append(taxon)
        except:
            print "Failed to add to TaxaCollection.  Item must be of type Taxon."


class Taxon():
    def __init__(self, taxonID = "", taxonCode = "", taxonName = "", author = "", extinct = "", taxaGroup = "", ecolGroup = "",
                 higherTaxonID = "", publicationID = "", notes = ""):
        self.taxonID = taxonID
        self.taxonCode = taxonCode
        self.taxonName = taxonName
        self.author = author
        self.extinct = extinct
        self.taxaGroup = taxaGroup
        self.ecolGroup = ecolGroup
        self.higherTaxonID = higherTaxonID
        self.publicationID = publicationID
        self.notes = notes


class SampleDataCollection():
    def __init__(self):
        self.items = []
    def addSample(self, S):
        try:
            assert isinstance(S, Sample)
            self.items.append(S)
        except:
            print "Failed to add to SampleDataCollection.  Item must be of type Sample."

class SampleData():
    def __init__(self, taxagroup="", value="", variableUnits="", taxonName="", variableElement="", variableContext="",
                 sampleAge="", sampleAgeYounger="", sampleAgeOlder="", datasetID="", siteAltitude="", siteLatitudeN="",
                 siteLatitudeS="", siteLongitudeE="", siteLongitudeW=""):
        self.taxaGroup = taxagroup
        self.Value = value
        self.variableUnits = variableUnits
        self.taxonName = taxonName
        self.variableElement = variableElement
        self.variableContext = variableContext
        self.sampleAge = sampleAge
        self.sampleAgeYounger = sampleAgeYounger
        self.sampleAgeOlder = sampleAgeOlder
        self.datasetID = datasetID
        self.siteAltitude = siteAltitude
        self.siteLatitudeNorth = siteLatitudeN
        self.siteLatitudeSouth = siteLatitudeS
        self.siteLongitudeEast = siteLongitudeE
        self.siteLongitudeWest = siteLongitudeW


class Sample():
    def __init__(self, sampleID = "", sampleName = "", unitName = "", unitDepth = "", unitThickness = ""):
        self.sampleID = sampleID
        self.sampleName = sampleName
        self.unitName = unitName
        self.unitDepth = unitDepth
        self.unitThickness = unitThickness
        self.sampleAges = []
        self.sampleData = []

    def addAge(self, age):
        try:
            assert isinstance(age, SampleAge)
            self.sampleAges.append(age)
        except AssertionError:
            print "Failed to add to Sample.  Item mut be of type SampleAge."

    def addSampleData(self, sampleData):
        try:
            assert isinstance(sampleData, SampleData)
            self.sampleData.append(sampleData)
        except:
            print "Failed to add to Sample.  Item must be of type SampleData."

class SampleAge():
    def __init__(self, chronID = "", chronName = "", ageType="", age="", ageYounger = "", ageOlder = ""):
        self.chronID = chronID
        self.chronName = chronName
        self.ageType = ageType
        self.age =age
        self.ageYounger = ageYounger
        self.ageOlder = ageOlder

class DatasetDownload():
    def __init__(self, datasetID="", datasetName="", collUnitHandle="", collUnitType="", datasetType="",
                 neotomaLastSub="", defChronID=""):
        self.datasetID = datasetID
        self.datasetName = datasetName
        self.collUnitHandle = collUnitHandle
        self.collUnitType = collUnitType
        self.datasetType = datasetType
        self.neotomaLastSub = neotomaLastSub
        self.defChronologyID = defChronID
        self.site = Site() ##placeholder
        self.datasetPIs = []
        self.samples = []

    def addPI(self, pi):
        try:
            assert  isinstance(pi, datasetPI)
            self.datasetPIs.append(pi)
        except AssertionError:
            print "Failed to add to DatasetDownload.  Item must be of type datasetPI."

    def addSample(self, S):
        try:
            assert isinstance(S, Sample)
            self.samples.append(S)
        except AssertionError:
            print "Failed to add to DatasetDownload.  Item must be of type Sample."




