import generalFunction
from WSNs import *


fileDir = sys.argv[1]
fileName = "./simulation/Users/"+fileDir+"/graph.txt"
f = open(fileName, "r")
line = f.readline()
attrs = line.split(" ")
total = int(attrs[0])
anchorN = int(attrs[1])
rg = int(attrs[2])

tempWSN = WSNs(total, anchorN, rg, fileDir)

for i in range(0,total):
  coor = f.readline().split(" ")
  curMote = moteC(int(coor[0]), int(coor[1]), i, rg)
  tempWSN.moteList.append(curMote)
  if i <= anchorN:
    tempWSN.anchorList.append(curMote)
f.close()    

tempWSN.generateConnectedGraph()    
tempWSN.generateHopVector()
tempWSN.printNeighborFunc()
tempWSN.printPerfectTopo()
tempWSN.printHopFunc()



