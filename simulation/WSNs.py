from random import *
import sys
import math
import heapq
import generalFunction


class moteC:
    
    
    def __init__(self, locX,locY,moteID,radioRange=100):
        self.x = locX
        self.y = locY
        
        self.ID = moteID
        self.radioRange=radioRange
        self.neighborList = []
        self.routeeList =[]
        self.hop=dict()
        self.resetDic()
        self.broadcasted=0
        self.isAnchor=False
    def setTobeAnchor(self):
        self.isAnchor=True
        
    def resetDic(self):
        self.dic=[]
        for i in xrange(0,65535):
            self.dic.append(-1)    
    def addNeighbor(self, neighborMote):
        self.neighborList.append(neighborMote)
    
    def disToCoor(self,xx,yy):
        return math.sqrt(pow(self.x-xx,2)+pow(self.y-yy,2))
        
    def euclideanDist(self, mote): 
        return math.sqrt(pow(self.x-mote.x,2)+pow(self.y-mote.y,2))
        
    def isNeighbor(self, mote, threshold):
        return threshold>self.euclideanDist(mote)
        
    def addRoutee(self, rout):
        self.routeeList.append(rout)
        
    def setHop(self, index,hop):
        self.hop[index]=hop
        
    def getLocTup(self):
        return (self.x,self.y)    
    
    
    
        
    def broadcast(self,hops,ID):
        global totalSending
        global totalReceive
        if hops!=0 and self.dic[ID]<hops:
            self.dic[ID]=hops
            self.broadcasted+=1
            totalSending+=1
            for mote in self.neighborList:
                totalReceive+=1
                mote.broadcast(hops-1,ID)
                
    def geoBroadcast(self, p1,p2,p3,t1,t2,t3,ID,rH):
        global totalSending
        global totalReceive
        if p1==self.hop[0] and p2==self.hop[1] and p3==self.hop[2]:
            totalReceive+=1
            self.broadcast(rH+1,ID+1000)
            return
        if (abs(t1-p1)>=abs(t1-self.hop[0]) and abs(t2-p2)>=abs(t2-self.hop[1]) and abs(t3-p3)>=abs(t3-self.hop[2]) )and self.dic[ID]!=1:
            self.dic[ID] = 1
            self.broadcasted+=1
            totalSending+=1
            for mote in self.neighborList:
                totalReceive+=1

    def hopBasedBroadcast(self,messages):
        global totalSending
        global totalReceive
        totalReceive+=1
        if self.broadcasted==0:
            for message in messages:
                if self.checkIfBroadcast(message):
                    totalSending+=1
                    self.broadcasted=1
                    for mote in self.neighborList:
                        mote.hopBasedBroadcast(messages)
                    break
            
    def checkIfBroadcast(self,message):
        if len(message)==5:
            if self.hop[message[2]]<=message[4] and self.hop[message[0]]-self.hop[message[1]]<2*message[3] and self.hop[message[0]]-self.hop[message[1]]>2*(message[3]-1):
                return True
            else:
                return False
        
        elif len(message)==4:
            if self.hop[message[0]]<=message[2] and self.hop[message[1]]<=message[3] and self.hop[message[1]]>=message[2]-1:
                return True
            else:
                return False
        else:
            return False
            
            
            

class WSNs:

    def __init__(self, nodeNumber, anchorNumber,radioRange, fd):
        
        self.fileDir = fd
        self.defaultRatio=0.5
        self.locSet=set()
        self.moteList=[]
        self.anchorList=[]
        self.priorityCoverage=[]
        self.nodeNum=nodeNumber
        self.anchorNum=anchorNumber
        self.radioRange=radioRange
        self.x1=0
        self.y1=0
        self.x2=0
        self.y2=0
        self.leftTop=(0,0)
        self.rightBottom=(0,0)
        self.currentIndex=0



    def printHopFunc(self):
        rf = open("./simulation/Users/"+ self.fileDir +"/hopVector.h","w")
        
        rf.write("#ifndef HOPVECTOR_H\n")
        rf.write("#define HOPVECTOR_H\n")
        rf.write("void  getHopVector(uint8_t *id,uint8_t * a){\n")
        i=0
        for m in self.moteList[:]:

            rf.write("if(TOS_NODE_ID=="+str(i)+"){\n")
            j=0
            
            for key,value  in m.hop.iteritems():
                rf.write("    id["+str(j)+"] = " + str(key) + ";\n")
                rf.write("    a["+str(j)+"] = "+str(value)+";\n")
                j+=1
            rf.write("}\n")    
            i+=1
          
        rf.write("}\n")
        rf.write("#endif")
        rf.close()

    def printPerfectTopo(self):
        tof = open("./simulation/Users/"+ self.fileDir +"/perfectTopo.txt","w")
        i=0
        for mlist in self.graph_Matrix[:]:
            j=0
            for nM in mlist[:]:
                if i!=j and nM == 1:
                    tof.write("gain   ")
                    tof.write(str(i)+"   ")
                    tof.write(str(j)+"   ")
                    tof.write("-60\n")
                j+=1 
            i+=1
        tof.close() 
        
    def printTopoAll(self):
        ta = open("./simulation/graph.txt","w")
        
        for cmote in self.moteList[:]:
            ta.write(str(cmote.x)+" "+str(cmote.y)+"\n")
        ta.close()        

    def printNeighborFunc(self):
        nf = open("./simulation/Users/"+ self.fileDir +"/Neighbor.h","w")
        nt = open("./simulation/Users/"+ self.fileDir +"/allNeighbor.txt","w")
        nf.write("#ifndef NEIGHBOR_H\n")
        nf.write("#define NEIGHBOR_H\n")
        nf.write("void  getNeighbor(uint16_t * a){\n")
        i=0
        for m in self.moteList[:]:
            nf.write("if(TOS_NODE_ID=="+str(i)+"){\n")
            j=0
            for n in m.neighborList[:]:
                if j<20:
                    nf.write("    a["+str(j)+"] = "+str(n.ID)+";\n")
                j+=1
                nt.write(str(n.ID)+" ")
            nf.write("}\n")
            nt.write("\n")    
            i+=1
        nt.close()  
        nf.write("}\n")
        nf.write("#endif")
        nf.close()
    
    def anchorToNpArray(self):
        al=[]
        for aa in self.anchorList:
            al.append([aa.x,aa.y])
        return al
    
    def anchorDisToNpArray(self,areaSet):
        dis=self.findAllDisTup(areaSet)
        al=[]
        for s1 in xrange(0,self.anchorNum):
            al.append((self.anchorList[s1].ID,self.findHopDis1(self.anchorList[s1],dis[s1])))
        return al
        
    
    def getMote(self,ID):
        return self.moteList[ID]
        
    def generateMoteList(self,nodeNumber,x1,y1,x2,y2,radioRange):
        curNum=len(self.moteList)
        while curNum<nodeNumber:
            self.genMote(x1,y1,x2,y2,radioRange)
            curNum+=1
        
    def genLocTup(self,x1,y1,x2,y2):
        return (randint(x1,x2),randint(y1,y2))

    def genMote(self,x1,y1,x2,y2,radioRange):
        curT=()
        while True:
            curT = self.genLocTup(x1,y1,x2,y2)
            if curT not in self.locSet:
                self.locSet.add(curT)
                break
        curMote = moteC(curT[0],curT[1],self.currentIndex,radioRange)
        self.currentIndex+=1
        self.moteList.append(curMote)
        
    def pickAnchorNode(self,anchorNumber):
        curMax=len(self.moteList)
        curNum=0
        #curSet=set()
        while curNum<anchorNumber:
            #rIndex=randint(0,curMax-1)
            
            #while rIndex in curSet:
                #rIndex=randint(0,curMax-1)
            #curSet.add(rIndex)
            self.moteList[curNum].setTobeAnchor()
            self.anchorList.append(self.moteList[curNum])
            curNum+=1
            
    def generateConnectedGraph(self):
        self.graph_Matrix =[]
        i=0
        for outMote in self.moteList[:]:
            innerList =[]
            j=0
            for innerMote in self.moteList[:]:
                if outMote.isNeighbor(innerMote,self.radioRange) and i != j:
                    innerList.append(1)
                    outMote.addNeighbor(innerMote)
                else:
                    innerList.append(0)
                j+=1
            self.graph_Matrix.append(innerList)            
            i+=1 
        
            
    def generateHopVector(self):
        for mmm in self.anchorList:
            visited=set()
            queue =[mmm.ID]
            mmm.setHop(mmm.ID,0)
            loopCount=0
            curhop=0
            while queue:
                if loopCount>self.nodeNum:
                    return
                vertex = queue.pop(0)
                visited.add(vertex)
                if mmm.ID in self.moteList[vertex].hop:
                    curhop=self.moteList[vertex].hop[mmm.ID]
                for mote in self.moteList[vertex].neighborList[:]:
                    if mmm.ID in mote.hop and curhop+1<mote.hop[mmm.ID]:
                        mote.setHop(mmm.ID,curhop+1)
                    if mote.ID not in visited:
                        mote.setHop(mmm.ID,curhop+1)
                        visited.add(mote.ID)    
                        queue.append(mote.ID)
    
    def findNode(self,nodeID):
        for node in self.moteList:
            if node.ID ==nodeID:
                return node
        return None
    
    
    def genCircleInter(self,areaSet,cx,cy,cdis,inx1,iny1,inx2,iny2,ind1,ind2):
        iniSize=len(areaSet)
        itSet=set(areaSet)
        
        for s1 in xrange(0, self.anchorNum):
            curNode1=self.anchorList[s1]
            disTup=allDisTup[s1]
            farthestDis=disTup[0]
            nearestDis=disTup[1]
            hopDis=self.findHopDis1(curNode1,farthestDis)
            
            for h in xrange(nearestDis,farthestDis+1,hopDis):
                cx.append(curNode1.x)
                cy.append(curNode1.y)
                cdis.append(h)
            for s2 in xrange(0, self.anchorNum):
                if s1!=s2:
                    curNode2=self.anchorList[s2]
                    disTup2=allDisTup[s2]
                    farthestDis2=disTup2[0]
                    nearestDis2=disTup2[1]
                    hopDis2=(hopDis+self.findHopDis1(curNode2,farthestDis2))/2
                    hopBetween=curNode1.hop[curNode2.ID]
                    for RH in xrange(nearestDis,farthestDis+10,hopDis2):
                        for rH in xrange(abs(hpBetween-RH),farthestDis2+10,hopDis2):
                            inx1.append(curNode1.x)
                            iny1.append(curNode1.y)
                            inx2.append(curNode2.x)
                            iny2.append(curNode2.y)
                            ind1.append(RH)
                            ind2.append(rH)
   
                    
    def findAllDisTup(self,areaSet):
        res=[]
        for mote in self.anchorList:
            res.append(self.findFarthestDis(mote,areaSet))
        return res                
                    
                    
    def findFarthestDis(self, sNode, areaSet):
        sx=sNode.x
        sy=sNode.y
        farthestDis=0
        nearestDis=2147483
        for tup in areaSet:
            dis=(sx-tup[0])**2+(sy-tup[1])**2
            farthestDis=max(farthestDis,dis)
            nearestDis=min(nearestDis,dis)
        return (math.sqrt(farthestDis),math.sqrt(nearestDis))
        
        
        
        
        
        
        
        
        
        
        
    def findHopDis1(self,sNode,fDis):
        totalHops=0
        totalDis=0
        for nNode in self.anchorList:
            dis=sNode.euclideanDist(nNode)
            if dis<=3*fDis and nNode.ID in sNode.hop:
                totalHops+=sNode.hop[nNode.ID]
                totalDis+=dis
        if totalHops==0:
            totalHops=0
            totalDis=0
            for nNode in self.anchorList:
                dis=sNode.euclideanDist(nNode)
                totalHops=1
                if nNode.ID in sNode.hop:
                    totalHops+=sNode.hop[nNode.ID]
                totalDis+=dis
        return totalDis/totalHops
        
    def findCoverRatio(self,sNode,hp,hpDis,areaSet):
        covered=[]
        total=[]
        ratio=[]
        radius=int(hp*hpDis)
        for i in xrange(1, hp+1):
            covered.append(0)
            total.append(math.pi*((i*hpDis)**2))
        for tup in areaSet:
            pixDis=sNode.disToCoor(tup[0],tup[1])
            if pixDis<radius:
                covered[int(pixDis/hpDis)]+=1
        preCovered=0.0
        for i in xrange(0,hp):
            covered[i]+=preCovered
            preCovered=covered[i]
            ratio.append((1.0*covered[i]/total[i],1.0*covered[i]**2/total[i],covered[i]))
        return ratio
    
                 
    def findCoverRatio2(self,cn1,cn2,hpBetween,fht2,nht2,hopDis,areaSet):
        covered=dict()
        total=dict()
        ratio=dict()
        nearestRadius0=nht2[0]*hopDis
        nearestRadius1=nht2[1]*hopDis
        farthestRadius0=fht2[0]*hopDis
        farthestRadius1=fht2[1]*hopDis
        d=cn1.euclideanDist(cn2)
        for RH in xrange(nht2[0],fht2[0]+1):
            R=RH*hopDis
            Ravg=(1.0*RH-0.5)*hopDis
            ringTotal=math.pi*R**2-math.pi*(R-hopDis)**2
            massTotal=math.pi*R**2
            for rH in xrange(abs(hpBetween-nht2[0])+1,fht2[1]+2):
                r=rH*hopDis
                x=(d**2-r**2+R**2)/(2*d)
                
                if abs(x)>=R :
                    total[(RH,-rH)]=ringTotal
                elif abs(R+r-d)<=hopDis or abs(R+r-d)>=R-hopDis:
                    total[(RH,-rH)]=generalFunction.archArea(R,x)+generalFunction.archArea(r,d-x)
                    total[(RH,rH)]=massTotal-total[(RH,-rH)]
                else:
                    xavg=(d**2-r**2+Ravg**2)/(2*d)
                    theta=math.acos(xavg/Ravg)/math.pi
                    #theta=math.acos(x/R)/math.pi
                    total[(RH,-rH)]=ringTotal*theta
                    total[(RH,rH)]=ringTotal*(1.0-theta)
                    
        for RH in xrange(nht2[1],fht2[1]+1):
            R=RH*hopDis
            Ravg=(1.0*RH-0.5)*hopDis
            Rmin=(1.0*RH-1)*hopDis
            ringTotal=math.pi*R**2-math.pi*(R-hopDis)**2
            for rH in xrange(abs(hpBetween-nht2[1])+1,fht2[0]+2):
                r=rH*hopDis
                x=(d**2-r**2+R**2)/(2*d)
                
                if abs(x)>=R :
                    total[(-rH,RH)]=ringTotal
                elif abs(R+r-d)<=hopDis or abs(R+r-d)>=R-hopDis:
                    total[(-rH,RH)]=generalFunction.archArea(R,x)+generalFunction.archArea(r,d-x)
                    total[(-rH,-RH)]=massTotal-total[(-rH,RH)]
                else:
                    xavg=(d**2-r**2+Ravg**2)/(2*d)
                    theta=math.acos(xavg/Ravg)/math.pi
                    #theta=math.acos(x/R)/math.pi
                    total[(-rH,RH)]=ringTotal*theta
                    total[(-rH,-RH)]=ringTotal*(1.0-theta)
        for tup in areaSet:
            pixDis1=max(1,cn1.disToCoor(tup[0],tup[1]))
            pixDis2=max(1,cn2.disToCoor(tup[0],tup[1]))                       
            hop1=int((pixDis1-1)/hopDis)+1
            hop2=int((pixDis2-1)/hopDis)+1
            if (hop1,-hop2) in total:
                covered[(hop1,-hop2)]=covered.get((hop1,-hop2),0)+1
            if (hop1,hop2-1) in total:
                covered[(hop1,hop2-1)]=covered.get((hop1,hop2-1),0)+1
            if (-hop1,hop2) in total:
                covered[(-hop1,hop2)]=covered.get((-hop1,hop2),0)+1
            if (-hop1+1,-hop2) in total:
                covered[(-hop1+1,-hop2)]=covered.get((-hop1+1,-hop2),0)+1
                
        
        
        for key,cov in covered.iteritems():
            ratio[key]=(cov/total[key],cov**2/total[key],cov)
        
        return  ratio
        
        
        
                
def combineWSNs(wsnList):
    resMoteList=[]
    resAnchorList=[]
    for i in xrange(len(wsnList)):
        resMoteList+=wsnList[i].moteList
        resAnchorList+=wsnList[i].anchorList
        wsnList[i]=WSNs(0,0,0,0,0,0,0)
        
    gc.collect()    
    res=WSNs(0,0,0,0,0,0,0)
    res.moteList=resMoteList
    res.anchorList=resAnchorList
    res.nodeNumber=len(res.moteList)
    res.anchorNumber=len(res.anchorList)
    return res
