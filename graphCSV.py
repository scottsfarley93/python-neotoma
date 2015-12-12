import csv
import matplotlib.pyplot as plt
import scipy
import pandas
filename = "/Users/scottsfarley/downloads/tower.csv"
reader = csv.reader(open(filename, 'r'))
data = {}
i = 0
ages = []
rawAges = []
ageOld = []
ageYoung = []
depths = []
for row in reader:
   name = row[0]
   groups = row[1]
   type = row[2]
   if i == 0:
       ages = row
   else:
       data[name] = []
       j = 0
       for item in row:
           if j < 4:
               pass
           else:
               if row[j] == '':
                   val = 0
               else:
                   val = row[j]
               try:
                   val = float(val)
                   data[name].append(val)
               except Exception as e:
                  if "/" in val:
                     age1, age2, age3 = val.split("/")
                     ageOld.append(age1)
                     ageYoung.append(age2)
                     rawAges.append(age3)
           j +=1
   i += 1

oak =  data['Quercus']
tsuga = data['Tsuga']

##gather pine together
pinus = []
pine1 = data['Pinus undiff.']
pine2 = data['Pinus subg. Strobus']
pine3 = data['Pinus subg. Pinus']
i = 0
while i < len(pine1):
    pval = pine1[i] + pine2[i] + pine3[i]
    pinus.append(pval)
    i +=1

##calculate pollen sum
i = 0
sums = []
while i < len(oak):
    thisSum = 0
    for item in data:
        if 'Lycopodium' not in item:
            try:
                thisSum += data[item][i]
                print thisSum
            except Exception as e:
                print str(e)
    sums.append(thisSum)
    i += 1

##now normalize
i = 0
# while i < len(pinus):
#     try:
#         pinus[i] = (pinus[i] / sums[i]) * 100
#         oak[i] = (oak[i] / sums[i]) * 100
#
#     except:
#         pinus[i] = 0
#         oak[i] = 0
#     i += 1
div1x = [0, 400]
div1y = [6300, 6300]
div2x = [0, 400]
div2y = [4900, 4900]

pinus.pop()
oak.pop()
tsuga.pop()
plt.plot(pinus, ageOld, lw=0.5, label="Pinus (all)")
plt.plot(oak, ageOld, lw=0.5, label="Quercus")
plt.plot(tsuga, ageOld, lw=0.5, label="Tsuga")
plt.plot(div1x, div1y, lw=1, c='grey' )
plt.plot(div2x, div2y, lw=1, c='grey')
plt.legend()
plt.title("Tower Lake, Minnesota")
plt.xlabel("Raw Count")
plt.ylabel("Age (Radiocarbon BP)")
plt.show()

