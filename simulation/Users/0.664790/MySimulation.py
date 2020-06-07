
#
# * @author Xiaofei Cao
# * @date   Jan 18 2018 
# * Computer Science
# * Missouri University of Science and Technology

import sys
import os
from random import *
from TOSSIM import *
from SimHelper import *
from requestMsg import *
sys.stdout.flush()
t = Tossim([])
r = t.radio();


hopMsg=map(int, sys.argv[2].strip('[]').split(','))
target=int(sys.argv[1])
print "routing message is: " +str(hopMsg)
print "routing message size is: "+ str(len(hopMsg))
print "target: "+ str(target)




##########
#TOPOLOGY
##########
readTopology("./perfectTopo.txt",r)

motelist = []

numNodes = getMotelist("./graph.txt",motelist)
#print motelist
getNeighbor("./allNeighbor.txt",motelist,numNodes)


######################
#NOISE TRACE & BOOTING
######################

noise = open("../../Noise/superShortNoise.txt", "r")
#noise = open("Noise/meyer-heavy-short.txt", "r")
lines = noise.readlines()
for line in lines:
  str = line.strip()
  if (str != ""):
    val = int(str)
    
    for i in range(0, numNodes):
      t.getNode(i).addNoiseTraceReading(val)
noise.close() 

for i in range(0, numNodes):
  #print "Creating noise model for ",i;
  t.getNode(i).createNoiseModel();

for i in range(0, numNodes):
  #bootTime=1351217999+randint(100000,200000) * i;
  bootTime=1351217999;
  t.getNode(i).bootAtTime(bootTime);
  motelist[i].setBootTime(bootTime);
  #print "Boot Time for Node ",i, ": ",bootTime;
  





#########
#CHANNELS
#########

#EnergyURL = os.path.expanduser("~/Desktop/hopVectorSim/Energy.txt")
debugURL = os.path.expanduser("./debug.txt")

#bla = open(EnergyURL, "w")
debug = open(debugURL,"w")
#t.addChannel("ENERGY_HANDLER", bla)
t.addChannel("LocalTime", debug)



#t.addChannel("RequestReceive",sys.stdout)
#t.addChannel("BackReceive",sys.stdout)
#t.addChannel("DisReceive",sys.stdout)
#t.addChannel("Debug",sys.stdout)

##########
#EXEC LOOP
##########
pktNum=0
t.runNextEvent();
time=t.time();
            # 1000000000000 = 100 seconds
count=0


while (time + 1000000000000 > t.time()):
  if t.time()>=motelist[numNodes-1].bootTime +800000 and count==0:
    count+=1
    msg = requestMsg()
    msg.set_mode(27)
    msg.set_requestID(11)
    msg.set_dataSize(len(hopMsg))
    msg.set_routingMessage(hopMsg)


    pkt = t.newPacket()
    pkt.setData(msg.data)
    pkt.setType(msg.get_amType())
    pkt.setDestination(target)
    pkt.deliver(target, t.time() + 10000)
    pktNum+=1;
  t.runNextEvent()
  
  
debug.close()

