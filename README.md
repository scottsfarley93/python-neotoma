# python-neotoma
A programmatic interface to the neotoma database for the python programming language.  

Author: Scott Farley

November, 2015

## Summary
This package provides programmatic access to the neotoma paleoecological database using python to complete the REST API calls.  The API call responses are dropped into python objects that mirror the response structure from the API.  All endpoints except for getDBTables are active, allowing users to search for Taxa, Datasets, Sites, Contacts, SampleData, and Downloads.  The package mirrors the existing R api interface at <a href="https://github.com/ropensci/neotoma">R Open Sci </a>. A limited set of unit tests has been implemented to check valid inputs and return formats.

## Two Brief Examples

```python
import neotoma
from neotoma import API
# List all site names in the database between 1000 and 2000m altitude
sites = API.getSite(altmin=1000, altmax=2000) ##siteCollection
for site in sites.items: ##iterate over the siteCollection's items
  print site.siteName

# List all mammal taxa in the database
mammals = API.getTaxa(taxagroup="MAM")
for t in mammals.items:
  print t.taxonName
```

##Documentation
Documentation is under construction.

##Issue Tracking
Issues can be tracked using the GitHub issue tracking tool.

##Neotoma
More information about the neotoma paleoecological database can be found at <a href='neotomadb.org'>Neotoma.org</a>.
