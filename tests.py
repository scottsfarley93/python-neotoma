__author__ = 'scottsfarley'
##tests are based on R tests
import unittest
import API
import classes
import json
import urllib2

class test_API(unittest.TestCase):
    ##make sure the api is returning what is supposed to be returned
    def setUp(self):
        self.aa = json.load(urllib2.urlopen('http://api.neotomadb.org/v1/data/datasets?siteid=1'))
        self.bb = json.load(urllib2.urlopen('http://api.neotomadb.org/v1/data/datasets?gpid=756'))

    def test_API1(self):
        self.assertIsInstance(self.aa['data'], list)

    def test_API2(self):
        self.assertIsInstance(self.bb['data'], list)

    def test_API3(self):
        self.assertEqual(len(self.aa.keys()), 2)

    def test_API4(self):
        self.assertEqual(self.aa['success'], 1)

    def test_API5(self):
        self.assertGreater(len(self.aa['data']), 0)

    def test_API6(self):
        self.assertEqual(json.load(urllib2.urlopen("http://api.neotomadb.org/v1/data/datasets?banana"))['success'], 0)

    def test_API7(self):
        self.assertEqual(self.bb['success'], 1)

    def test_API8(self):
        self.assertGreater(len(self.bb['data']), 0)

class test_getDataset(unittest.TestCase):
    def test_getDataset1(self):
        self.assertRaises(TypeError, API.getDatasets(x='a'))

    def test_getDataset2(self):
        self.assertFalse(API.getDatasets(datasettype=10))

    def test_getDataset3(self):
        self.assertFalse(API.getDatasets(datasettype='banana'))

    def test_getDataset4(self):
        self.assertFalse(API.getDatasets(piid='a'))

    def test_getDataset5(self):
        self.assertFalse(API.getDatasets(altmin='low'))

    def test_getDataset6(self):
        self.assertFalse(API.getDatasets(altmax='low'))

    def test_getDataset7(self):
        self.assertFalse(API.getDatasets(loc=10))

    def test_getDataset8(self):
        self.assertFalse(API.getDatasets(loc=['a', 'b', 'c']))

    def test_getDataset9(self):
        self.assertFalse(API.getDatasets(loc=['a', 'b', 'c', 'd']))

    def test_getDataset10(self):
        self.assertFalse(API.getDatasets(ageold='min'))

    def test_getDataset11(self):
        self.assertFalse(API.getDatasets(ageyoung="max"))

    def test_getDataset12(self):
        self.assertFalse(API.getDatasets(ageof="taxon")) ##not sure about this test --> this will fail in my version

    def test_getDataset13(self):
        self.assertFalse(API.getDatasets(subdate=10)) ##todo: make sure this returns false

    def test_getDataset14(self):
        self.assertIsInstance(API.getDatasets(gpid=10), classes.DatasetCollection)
    ##todo: add more positive validation here



class testGetContacts(unittest.TestCase):
    def test_getContact1(self):
        self.assertFalse(API.getContacts(contactid='aaa'))
    def test_getContact2(self):
        self.assertFalse(API.getContacts(contactname=12))
    def test_getContact3(self):
        self.assertFalse(API.getContacts(contactstatus=1))
    def test_getContact4(self):
        self.assertFalse(API.getContacts(familyname=12))
    def test_getContact5(self):
        self.assertIsInstance(API.getContacts(contactid=1), classes.ContactCollection)
    def test_getContact6(self):
        self.assertEqual(len(API.getContacts(contactid=1).items), 1)
    def test_getContact7(self):
        self.assertIsInstance(API.getContacts(familyname="Smith"), classes.ContactCollection)
    def test_getContact8(self):
        self.assertIsInstance(API.getContacts(contactname="*Smith*"), classes.ContactCollection)


class test_getDownload(unittest.TestCase):
    def test_getDownload1(self):
        self.assertFalse(API.getDatasetDownload('a'))
    def test_getDownload2(self):
        self.assertFalse(API.getDatasetDownload(['a', 'b']))
    def test_getDownload3(self):
        self.assertTrue(API.getDatasetDownload(1))
    def test_getDownload4(self):
        self.assertEqual(len(API.getDatasetDownload(1).items), 1)
    def test_getDownload5(self):
        self.assertEqual(len(API.getDatasetDownload([1, 2]).items), 2)
    def test_getDownload6(self):
        self.assertEqual(len(API.getDatasetDownload((1, 2, 3)).items), 3)
    def test_getDownload7(self):
        self.assertIsInstance(API.getDatasetDownload(1), classes.DatasetCollection)
    def test_getDownload8(self):
        ##need to implement isNumeric here
        ds = API.getDatasetDownload(3031).items[0]
        chronID = str(ds.defChronologyID) ## make string so we can use the isdigit method
        self.assertTrue(chronID.isdigit())
    def test_getDownload9(self):
        ds= API.getDatasetDownload(3031).items[0]
        did = str(ds.datasetID)
        self.assertTrue(did.isdigit())
    def test_getDownload10(self):
        ds = API.getDatasetDownload(6000).items[0]
        chronID = str(ds.defChronologyID) ## make string so we can use the isdigit method
        self.assertTrue(chronID.isdigit())
    def test_getDatasetDownload11(self):
        ds = API.getDatasetDownload(6000).items[0]
        did = str(ds.datasetID)
        self.assertTrue(did.isdigit())
    def test_getDatasetDownload12(self):
        dc = API.getDatasetDownload(17387) ##collection
        ds = dc.items[0]##individual dataset
        chronID = ds.defChronologyID
        self.assertEqual(chronID, 9726)
    def test_getDatasetDownload13(self):
        self.assertIsInstance(API.getDatasetDownload(1).items[0], classes.DatasetDownload)
    def test_getDatasetDownload14(self):
        a = API.getDatasetDownload([1,2,3,4])
        i = 0
        while i < len(a.items):
            b = a.items[i]
            self.assertIsInstance(b, classes.DatasetDownload) ##make sure all items in list are download
            i +=1

class test_getPublications(unittest.TestCase):
    def test_getPublications1(self):
        self.assertFalse(API.getPublications(pubid='aaa'))
    def test_getPublications2(self):
        self.assertFalse(API.getPublications(contactid='aaa'))
    def test_getPublications3(self):
        self.assertFalse(API.getPublications(datasetid='aaa'))
    def test_getPublications4(self):
        self.assertFalse(API.getPublications(author=1))
    def test_getPublications5(self):
        self.assertFalse(API.getPublications(pubtype="banana"))
    def test_getPublications6(self):
        self.assertFalse(API.getPublications(year='aaa'))
    def test_getPublications7(self):
        self.assertIsInstance(API.getPublications(pubid=1), classes.PublicationCollection)
    def test_getPublications8(self):
        self.assertIsInstance(API.getPublications(contactid=10).items[0], classes.Publication)
    def test_getPublications9(self):
        col = API.getPublications(contactid=10).items[0]
        authors = col.authors
        a = authors[0]
        self.assertIs(a, classes.Author)

class test_getTaxa(unittest.TestCase):
    def test_getTaxa1(self):
        self.assertFalse(API.getTaxa(taxonID='aaa'))
    def test_getTaxa2(self):
        self.assertFalse(API.getTaxa(taxonName=1213))
    def test_getTaxa3(self):
        self.assertFalse(API.getTaxa(status='banana'))
    def test_getTaxa4(self):
        self.assertFalse(API.getTaxa(taxagroup="banana"))
    def test_getTaxa5(self):
        self.assertFalse(API.getTaxa(taxagroup=1))
    def test_getTaxa6(self):
        self.assertIsInstance(API.getTaxa(taxagroup="MAM"), classes.TaxaCollection)
    def test_getTaxa7(self):
        self.assertIsInstance(API.getTaxa(taxagroup="Testate amoebae"), classes.TaxaCollection)
    def test_getTaxa8(self):
        self.assertIsInstance(API.getTaxa(taxonID=1), classes.TaxaCollection)
    def test_getTaxa9(self):
        self.assertIsInstance(API.getTaxa(taxonID=1).items[0], classes.Taxon)





