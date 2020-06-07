from Tkinter import *
import time
import os




shapeList=[]
gui = Tk()
gui.wm_title("Broadcasting simulation")
gui.geometry("2400x2000")
c = Canvas(gui,bg='white',width=2380,height=2000)
c.pack()

topoFile = open("./simulation/graph.txt","r")
topodata = topoFile.readlines()
for line in topodata:
    words = line.split()
    
    shapeList.append(c.create_oval(int(words[0])-5,int(words[1])-5,int(words[0])+5,int(words[1])+5))
gui.update()

listenList=[]
transmitList=[]
for shape in shapeList:
    listenList.append(0)
    transmitList.append(0)

debugURL = os.path.expanduser("~/Desktop/hopVectorSim/debug.txt")

debug = open(debugURL,"r")
visData = debug.readlines()
preTime = 0;
total=0
totalReceived=0
totalTransmit=0
for visLine in visData:
    data = visLine.split()
    
    mode = data[2]
    node = int(data[3])
    ctime = int(data[5])
    #print mode
    #print node
    
    dt= ctime - preTime
    preTime = ctime
    #print dt 
    total+=dt
    dt=max(dt/1000,0.001)
    if mode == '000,':
        c.itemconfig(shapeList[node],fill='green')
    if mode == '111,':
        c.itemconfig(shapeList[node],fill='red')
        totalTransmit+=1
    totalReceived+=1    
    gui.update()
    time.sleep(dt)
    
print "Broadcast takes total: " + str(total) +"ms"   
print "Number of receiving nodes: "+ str(totalReceived)
print "Number of transmiting nodes: "+ str(totalTransmit) 
print " simulating finish"

gui.mainloop()
