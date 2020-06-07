from random import *
import math
import sys
class moteC:
    
    
    def __init__(self, locX,locY,moteID):
        self.x = locX
        self.y = locY
        self.ID = moteID
        self.neighborList = []
        self.routeeList =[]
    def addNeighbor(self, neighborMote):
        self.neighborList.append(neighborMote)
        
    def euclideanDist(self, mote): 
        return math.sqrt(pow(self.x-mote.x,2)+pow(self.y-mote.y,2))
        
    def isNeighbor(self, mote, threshold):
        return threshold>self.euclideanDist(mote)
        
    def addRoutee(self, rout):
        self.routeeList.append(rout)
        
    def setHop(self, hop):
        self.hop = hop
        
    def setBootTime(self,bootTime):
        self.bootTime = bootTime
        
        
def readTopology(fileName,r):

    f = open(fileName, "r")

    lines = f.readlines()
    i =0
    for line in lines:
        s = line.split()
        
        if (len(s) > 0):
            if (s[0] == "gain"):
      
                #print " ", s[1], " ", s[2], " ", s[3];
                r.add(int(s[1]), int(s[2]), float(s[3]));
    f.close()
    
    
    
def getMotelist(fileName, ml):
    f = open(fileName, "r")
    lines = f.readlines()
    i =-1
    for line in lines:
        if i>=0:
            s = line.split()
            if(len(s) >0):
                ml.append(moteC(int(s[0]),int(s[1]),i))
        i+=1
    f.close()
    return i
            
def getNeighbor(fileName, ml,nN):
    f = open(fileName, "r")
    lines = f.readlines()
    i =0
    for line in lines:
        s = line.split()
        if len(s)>0 and i<nN:
            for nei in s:
                #print int(nei)
                ml[i].addNeighbor(ml[int(nei)])
        i+=1
    f.close()
    
def getHop(fileName, ml,nN):
    f = open(fileName, "r")
    lines = f.readlines()
    i = 0
    for line in lines:
        s = line.split()
        if len(s)>0 and i<nN:
            ml[i].setHop(int(s[0]))
            for j in xrange(1,len(s)):
                ml[i].addRoutee(ml[int(s[j])])
        i+=1
    f.close()  
    
def findPath(destNode): 
    resStack = [destNode.ID]
    current = choice(destNode.routeeList)
    while current.ID !=0:
        resStack.append(current.ID)
        current = choice(current.routeeList)
    resStack.append(0)
    return resStack

def findMiniHopCenter(motelist, node,targetList):
    hop = findHop(node, targetList)
    res = node
    buf = []
    visited = {node}
    for nNode in node.neighborList:
        if nNode not in visited:
            visited.add(nNode)
            chop = findHop(nNode,targetList)
            if chop < hop:
                hop = chop
                res = nNode
        for nnNode in nNode.neighborList:
            if nnNode not in visited:
                visited.add(nnNode)
                chop = findHop(nnNode,targetList)
                if chop < hop:
                    hop = chop
                    res = nnNode
      
    return (hop, res)
    
def findHop(node, targetList):
    res=0
    for target in targetList:
        chop = bfs(target, node)
        res = chop if chop > res else res
    
    return res
    
def bfs(target, node):
    queue=[node]
    visited={node}
    hop=0
    while True:
        buf = []
        for n in queue:
            if n.ID == target.ID: return  hop
            for nei in n.neighborList:
                if nei not in visited:
                    visited.add(nei)
                    buf.append(nei)
        del queue[:]
        queue=[i for i in buf]
        hop+=1;
        if hop>10 : return hop   
                   
def getCenter(x,y,areaList):
    if not areaList.any():
        return []
    dis = pow(x-areaList[0].x,2)+pow(y-areaList[0].y,2) 
    res = areaList[0]
    for node in areaList:
        curDis = pow(x-node.x,2)+pow(y-node.y,2)    
        if dis > curDis:
            dis = curDis
            res = node
    return res
                    
