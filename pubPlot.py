__author__ = 'scottsfarley'
import API
import matplotlib.pyplot as plt
from collections import Counter


pubReturn = API.getPublication()
pubs = pubReturn.items
years = []
for item in pubs:
    years.append(item.Year)

c = Counter(years)
x = []
y = []
for item in c:
    try:
        x.append(int(item))
        y.append(int(c[item]))
    except:
        pass

plt.bar(x, y)
plt.title("Publications in Neotoma")
plt.xlabel("Year")
plt.ylabel("Number of Publications")
plt.xlim([min(x), max(x)])
plt.show()