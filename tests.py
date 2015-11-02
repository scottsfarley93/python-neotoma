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

