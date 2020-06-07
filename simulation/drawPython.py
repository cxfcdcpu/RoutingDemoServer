from Tkinter import *
from tkColorChooser import askcolor
from WSNs import *
from functools import partial
import tkFont
import math
from multiprocessing import Pool
import gc
from generalFunction import *
from cycleInter import *
import random
import time
import cycleCuda as cCuda
from numba import cuda
import numpy as np
import os
import copy
from numba import float32
from numba import int32
import cycleInter as ci
from operator import itemgetter
import datetime
from PIL import Image
from PIL import ImageDraw
from PIL import ImageColor,ImageFont

totalSending=0;
totalReceive=0;



           
def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = _create_circle 

class Paint(object):

    default_node_number=1300
    default_anchor_number=20
    default_radio_range=100
    default_width=1800
    default_length=1700
    thread=6
    moteSize=2
    canvasWidth=2400
    canvasHeight=2000
    screenWidth=2400
    screenHeight=2000
    DEFAULT_PEN_SIZE = 10.0
    DEFAULT_COLOR = 'blue'
    counter = 0
    def __init__(self):
        #self.default_font = tkFont.nametofont("TkDefaultFont")
        #self.default_font.metrics(fixed=1)

        self.image1 = Image.new("RGB", (self.canvasWidth, self.canvasHeight), 'white')
        self.draw1 = ImageDraw.Draw(self.image1)
        
        self.offsetX=20
        self.offsetY=20
        self.final_msg=[]
        self.B=[]
        self.C=[]
        self.messageArea=dict()
        self.setToShowed=set()
        self.priorityCoverage=[]
        self.messageButtonList=[]
        self.step1Results=[]
        self.WSN=[]
        self.routingArea=[]
        self.routingAreaSet=set()
        self.nodeHopVector=[]
        self.old_node=-1
        self.root = Tk()
        self.nodeDic=dict()
        self.trace=[]
        self.msgRes=[]
        self.root.wm_title("Broadcasting Demo")
        self.helv36 = tkFont.Font(family='Helvetica', size=28, weight='bold')
        self.helv16 = tkFont.Font(family='Helvetica', size=16, weight='bold')
        self.messageIndex=0
        self.frame=Frame(self.root,width=self.screenWidth,height=self.screenHeight)
        self.frame.grid(row=1,columnspan=12)
        self.c = Canvas(self.frame, bg='white',width=self.canvasWidth,height=self.canvasHeight)
        #self.c.config(scrollregion = self.c.bbox("all"))
        
        
        hbar=Scrollbar(self.frame,orient=HORIZONTAL)
        hbar.pack(side=BOTTOM,fill=X)
        hbar.config(command=self.c.xview)
        vbar=Scrollbar(self.frame,orient=VERTICAL)
        vbar.pack(side=RIGHT,fill=Y)
        vbar.config(command=self.c.yview)
        
        self.c.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.c.pack(side=LEFT,expand=True,fill=BOTH)
        
        
        self.pen_button = Button(self.root, text='pen', command=self.use_pen,font=self.helv36)
        self.pen_button.grid(row=0, column=0)

        self.brush_button = Button(self.root, text='HopInfo', command=self.use_brush,font=self.helv36)
        self.brush_button.grid(row=0, column=1)

        self.color_button = Button(self.root, text='color', command=self.choose_color,font=self.helv36)
        self.color_button.grid(row=0, column=2)

        self.eraser_button = Button(self.root, text='eraser', command=self.use_eraser,font=self.helv36)
        self.eraser_button.grid(row=0, column=3)
        
        self.clear_all_button = Button(self.root,text='Clear', command=self.clearAll,font=self.helv36)
        self.clear_all_button.grid(row=0,column=4)
        
        
        self.Cbutton = Button(self.root, text="Generate WSNs", command=self.create_window,font=self.helv36)
        self.Cbutton.grid(row=0,column=5)

    
        
        

        self.choose_size_button = Scale(self.root, from_=10, to=100, orient=HORIZONTAL)
        self.choose_size_button.grid(row=0, column=6)
        

        self.Dbutton = Button(self.root, text="Debug", command=self.debug,font=self.helv36)
        self.Dbutton.grid(row=0,column=7)
        
        self.Rbutton = Button(self.root, text="routingMSG", command=self.genRoutingMSG,font=self.helv36)
        self.Rbutton.grid(row=0,column=8)
        
        self.Sbutton = Button(self.root, text="Search WSNs", command=self.search_window,font=self.helv36)
        self.Sbutton.grid(row=0,column=9)

        self.setup()
        self.root.mainloop()

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = self.pen_button
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)



    #def displayHopVector(self,x,y):
    def genRoutingMSG(self):
        self.msgRes=[]
        self.broadcastMessages=[]
        currentDT = datetime.datetime.now()
        cp=self.getCrop()
        image2=self.image1.crop(cp)
        image2.thumbnail((64,int(64*(cp[3]-cp[1])/(cp[2]-cp[0]))))
        image2.save(str(currentDT.minute)+str(currentDT.second)+".png")
        
        if self.WSN:
            #self.refineRoutingArea()

            locationSet=self.WSN.anchorToNpArray()
            idSet=self.WSN.anchorDisToNpArray(self.routingAreaSet)
            disSet=self.WSN.findAllDisTup(self.routingAreaSet)
            '''
            print "locationSet"
            print locationSet
            print "idSet"
            print idSet
            print "disSet"
            print disSet
            '''
            hopSet=[]
            dindex=0
            for dS in disSet:
                hopSet.append((int(dS[1]/idSet[dindex][1]),int(dS[0]/idSet[dindex][1])))
                dindex+=1
                
            print "hopSet"
            print hopSet
            
            npArea=np.zeros((len(self.routingAreaSet),2),dtype=np.float32)
            index=0
            for tup in self.routingAreaSet:
                
                npArea[index,0]=tup[0]
                npArea[index,1]=tup[1]
                index+=1
            
            
                #self.anyCycle(tup,1)    
            
            
                
            ps=[]    
            ps.append(idSet)
            ps.append(locationSet)
            ps.append(hopSet)
            _start=time.time() 

            #print ps
            result=[]  
            result=ci.twoCycleQueueGen(ps)
            
            idList=result[0]
            dataList=result[1]
                
            C=np.array(dataList,dtype=np.float32)
            D=np.array(idList,dtype=np.float32)
            
            #print C
            print C.shape
            cuda.select_device(0)
            dataSize=C.shape[0]
            output=np.zeros((dataSize,13),dtype=np.float32)
            
         

            d_data=cuda.to_device(C)
            d_output1=cuda.to_device(output)
            d_id=cuda.to_device(D)
            d_area=cuda.to_device(npArea)

            cCuda.bestTwoCycle[dataSize/128+1,128](d_data,d_area,d_id,d_output1)
            
            rr=d_output1.copy_to_host()
            res3=rr.tolist()
            res3.sort(reverse=True)
            
              
            
            print time.time()-_start
            
            '''
            
            

            rr=[]
            
            
            '''
            result=[]
            C=[]
            D=[]
            output=[]            
            gc.collect()
            cuda.current_context().reset() 
            
            _start=time.time() 
            ps=[]

             
            j=0.;
            for i in range(8):
                ids= copy.deepcopy(idSet)
                locs= copy.deepcopy(locationSet)
                hset= copy.deepcopy(hopSet)
                
                portion=(j/8,(j+1)/8)
                j+=1
                ps.append((ids,locs,hset,portion))
            
            #print "ps"
            #print ps
            result=[]               
            pool=Pool(processes=8)
            result=pool.map(ci.hyperQueueGen,ps)
            
            
            
            idList=[]
            dataList=[]
            for poss in result:
                idList+=poss[0]
                dataList+=poss[1]
            #print "idList"    
            #print idList

            C=np.array(dataList,dtype=np.float32)
            D=np.array(idList,dtype=np.float32)
            
            #print C
            print C.shape
            cuda.select_device(0)
            dataSize=C.shape[0]
            output=np.zeros((dataSize,17),dtype=np.float32)
            print "cpu time: " +str(time.time()-_start)
            _start=time.time()

            d_data2=cuda.to_device(C)
            d_output2=cuda.to_device(output)
            d_id2=cuda.to_device(D)
            d_area2=cuda.to_device(npArea)
            print "starting calculate the best Hyperbola"
            cCuda.bestHyper[dataSize/128+1,128](d_data2,d_area2,d_id2,d_output2)


            rr2=d_output2.copy_to_host()
            res4=rr2.tolist()
            res4.sort(reverse=True)
            

            
            print "Gpu time: " +str(time.time()-_start)
            
            newArea=[]
            
            if res4[0]>res3[0]:
                print res4[0]
                self.msgRes.append(res4[0])
                newArea=self.newArea2(res4[0],self.routingAreaSet)

            else:
                print res3[0]
                self.msgRes.append(res3[0])
                newArea=self.newArea1(res3[0],self.routingAreaSet)
            '''    

            rr2=[]
            
            
            '''
            result=[]
            C=[]
            D=[]
            output=[]
            gc.collect()
            cuda.current_context().reset()                 
            
            while len(newArea)>0.15*len(self.routingAreaSet):
                _start_time=time.time()
                print 1.0*len(newArea)/len(self.routingAreaSet)
                l1=280000
                l2=580000
                if len(res3)<l1:
                    l1=len(res3)-1
                if len(res4)<l2:
                    l2=len(res4)-1
                    
                    
                print 'l1 is'+str(l1)
                print 'l2 is'+str(l2)
                res3.sort(key=itemgetter(7),reverse=True)
                res4.sort(key=itemgetter(7),reverse=True)
                    
                data1=np.array(res3[0:l1],dtype=np.float32)
                data2=np.array(res4[0:l2],dtype=np.float32)
                np_newArea=np.array(newArea,dtype=np.float32)
                output1=np.zeros((l1,13),dtype=np.float32)
                output2=np.zeros((l2,17),dtype=np.float32)
                
                d_newArea1=cuda.to_device(np_newArea)            
                d_data1=cuda.to_device(data1)
                d_output1=cuda.to_device(output1)
                cCuda.goOver1[l1/128+1,128](d_data1,d_newArea1,d_output1)
                
                rr=d_output1.copy_to_host()
                res3=rr.tolist()
                res3.sort(reverse=True)
                

                
                d_newArea2=cuda.to_device(np_newArea)
                d_data2=cuda.to_device(data2)
                d_output2=cuda.to_device(output2) 
                cCuda.goOver2[l2/128+1,128](d_data2,d_newArea2,d_output2)
                
                rr2=d_output2.copy_to_host()
                res4=rr2.tolist()
                res4.sort(reverse=True)                
                if res4[0]>res3[0]:
                    newArea=self.newArea2(res4[0],newArea)
                    self.msgRes.append(res4[0])
                    print res4[0]
                    
                else:
                    newArea=self.newArea1(res3[0],newArea)
                    self.msgRes.append(res3[0])
                    print res3[0]
                print time.time()-_start_time
                
            #print self.msgRes    
                
                

    def newArea1(self,data,oldArea):
        res=[]
        
        x1=data[8]
        y1=data[9]
        x2=data[10]
        y2=data[11]
        r1=data[3]
        r2=data[4]
        r3=data[5]
        rr3=r3*r3
        rr1=r1*r1
        rr2=r2*r2
        for tup in oldArea:
            i=tup[0]
            j=tup[1]
            di1=x1-i
            dj1=y1-j
            di2=x2-i
            dj2=y2-j
            if not (di1*di1+dj1*dj1<=rr1 and di1*di1+dj1*dj1>rr3 and di2*di2+dj2*dj2<=rr2) :
                res.append([i,j])
        return res        
    
    def newArea2(self,data,oldArea):
        res=[]
        x=data[13]
        y=data[14]
        r=data[6]
        a=data[4]
        a2=data[5]
        
        h1x=data[9]
        h1y=data[10]
        h2x=data[11]
        h2y=data[12]

        rr=r*r    
        for tup in oldArea:
            i=tup[0]
            j=tup[1]
            di=x-i
            dj=y-j
            if not (di*di+dj*dj<=rr and gf.euDis((i,j),(h1x,h1y))-gf.euDis((i,j),(h2x,h2y))<=2*a and gf.euDis((i,j),(h1x,h1y))-gf.euDis((i,j),(h2x,h2y))>=2*a2):
                res.append([i,j])
        return res

    
    def anyHyperbola(self,h1,h2,dis):
        shapeList=[]
        hn1=(h1[0],h1[1])
        hn2=(h2[0],h2[1])
        shapeList.append(self.anyCycle(h1,5))
        shapeList.append(self.anyCycle(h2,5))
        for x in xrange(self.default_width):
            for y in xrange(self.default_length):
                if abs(gf.euDis((x,y),hn1)-gf.euDis((x,y),hn2)-2*dis)<0.5:
                    shapeList.append(self.c.create_oval(x-1,y-1,x+1,y+1,fill="red",outline="red"))
        return shapeList                
    
    def anyCycle(self,c,r):
        cn=(c[0],c[1])
        return self.c.create_oval(cn[0]-r,cn[1]-r,cn[0]+r,cn[1]+r,outline="red")
                
    def refineRoutingArea(self):
        oldTuple=()
        for curTuple in self.routingArea:
            if oldTuple:
                self.refineHelper(oldTuple,curTuple)
            oldTuple=curTuple
            
    def refineHelper(self,oldTuple,curTuple):
        #self.pointArea(oldTuple)
        #self.pointArea(curTuple)
        sx=min(oldTuple[0],curTuple[0])-self.line_width/2
        ex=max(oldTuple[0],curTuple[0])+self.line_width/2
        sy=min(oldTuple[1],curTuple[1])-self.line_width/2
        ey=max(oldTuple[1],curTuple[1])+self.line_width/2
        
        for x in xrange(sx,ex+1):
            for y in xrange(sy,ey+1):
                if (x,y) not in self.routingAreaSet:
                    dis=pointToLineDisTup(oldTuple,curTuple,x,y)
                    if dis<=self.line_width:
                        self.routingAreaSet.add((x,y))
                        self.B.append(x)
                        self.C.append(y)
                    
    def pointArea(self,curTuple):
        '''
        sx=max(0,curTuple[0]-self.line_width/2)
        ex=min(self.default_width,curTuple[0]+self.line_width/2)
        sy=max(0,curTuple[1]-self.line_width/2)
        ey=min(self.default_length,curTuple[1]+self.line_width/2)
        '''
        sx=curTuple[0]-self.line_width/2
        ex=curTuple[0]+self.line_width/2
        sy=curTuple[1]-self.line_width/2
        ey=curTuple[1]+self.line_width/2
        
        for x in xrange(sx, ex+1):
            for y in xrange(sy, ey+1):
                if ((x-curTuple[0])**2+(y-curTuple[1])**2)<=((self.line_width**2)/4):
                    self.routingAreaSet.add((x,y))    
    
    
    
    def getCrop(self):
        sx=99999
        sy=99999
        ex=0
        ey=0
        for ct in self.routingAreaSet:
            sx=min(ct[0],sx)
            sy=min(ct[1],sy)
            ex=max(ct[0],ex)
            ey=max(ct[1],ey)
        return [sx+self.line_width/2,sy+self.line_width/2,ex-self.line_width/2,ey-self.line_width/2]
    
    
    
    
    def search_window(self):
        
        self.showNum=10
        self.messageButtonList=[]
        self.messageIndex=0
        self.msgFlag=[0]
        self.eleDic=dict()
        self.totalRoutingArea=[]
        if self.Sbutton['state']==DISABLED:
            return
        self.Sbutton['state']=DISABLED
        self.t = Toplevel(self.root,height=500,width=2000)
        
        
        self.t.protocol("WM_DELETE_WINDOW", self.on_closingS)
        self.t.wm_title("Search Wireless sensor network")
        self.messageLabel=Label(self.t, text="", font=self.helv16)
        if self.msgRes:
            self.messageLabel.config(text=str(self.msgRes[0]))
            self.msgFlag*=len(self.msgRes)
            
        lable_node_number = Label(self.t, text="search node ID:    " ,font=self.helv16)
        lable_node_number.grid(row=0, column=0)
        enter_node_ID=Entry(self.t)
        enter_node_ID.grid(row=0,column=1)
        searchID_button=Button(self.t,text='Search', command=lambda: self.clickNode(int(enter_node_ID.get())),font=self.helv16)
        searchID_button.grid(row=0,column=2)
       
        self.messageLabel.grid(row=1,columnspan=3)
        
        prev_button=Button(self.t,text='<--',command=lambda:self.changeOffset(-1),font=self.helv16)
        next_button=Button(self.t,text='-->',command=lambda:self.changeOffset(1),font=self.helv16)
        total_button=Button(self.t,text="find Total Area", command=self.findTotalArea,font=self.helv16)
        self.simulate_button=Button(self.t,text="Simulate with Tossim",command=self.simulateWithTossim,font=self.helv16)
        self.current_button=Button(self.t,text="0",command=self.demoArea,font=self.helv16)
        
        prev_button.grid(row=2,column=0)
        self.current_button.grid(row=2,column=1)
        next_button.grid(row=2,column=2)
        total_button.grid(row=3,column=0)
        self.simulate_button.grid(row=3,column=1)
        
            
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        
        yoff= 500
        self.t.geometry("%dx%d+%d+%d" % (1600, 500, x + self.default_width/2,yoff))
        
    def simulateWithTossim(self):
        msg1=[]
        msg2=[]
        #final_msg=[]
        if self.msgRes and len(self.msgRes)>0:
            for msg in self.msgRes:
                rm=[]
                if len(msg)>14:
                    rm.append(int(msg[1]))
                    rm.append(int(msg[2]))
                    rm.append(int(msg[3]))
                    rm.append(int(round(msg[4]/msg[15])))
                    rm.append(int(round(msg[6]/msg[16])))
                    msg1.append(rm)
                else:
                    rm.append(int(msg[1]))
                    rm.append(int(msg[2]))
                    rm.append(int(round(msg[3]/msg[12])))
                    rm.append(int(round(msg[4]/msg[12])))
                    msg2.append(rm)
            for msg in msg1:
                self.final_msg+=msg
            self.final_msg.append(255)
            for msg in msg2:
                self.final_msg+=msg
                
            print self.final_msg
            self.activate_button(self.simulate_button)
            self.t.wm_state('iconic')
            
            
            
            
            
        return    
        
    def findTotalArea(self):
        if self.totalRoutingArea and len(self.totalRoutingArea)>0:
            for area in self.totalRoutingArea:
                self.c.delete(area)
                self.totalRoutingArea=[]
        else:        
            if self.msgRes:
                for x in xrange(1, self.canvasWidth,2):
                    for y in xrange(1, self.canvasHeight,2):
                        for msg in self.msgRes:
                            if len(msg)>14:
                                if self.inHyper((x,y),msg):
                                    self.totalRoutingArea.append(self.anyCycle((x,y),1))
                                    break    
                            else:
                                if self.inCycle((x,y),msg):
                                    self.totalRoutingArea.append(self.anyCycle((x,y),1))
                                    break
            
        
    def inHyper(self,tup,routing):
        h1=self.WSN.getMote(int(routing[1])).getLocTup() 
        h2=self.WSN.getMote(int(routing[2])).getLocTup() 
        c=self.WSN.getMote(int(routing[3])).getLocTup()
        a=routing[4]
        a2=routing[5]
        r=routing[6]
        dis=gf.euDis(tup,h1)-gf.euDis(tup,h2)  
        if gf.euDis(tup,c)<r and dis<2*a and dis>2*a2:
            return True
        return False
    
    def inCycle(self,tup,routing):
        c1=self.WSN.getMote(int(routing[1])).getLocTup() 
        c2=self.WSN.getMote(int(routing[2])).getLocTup() 
        r1=routing[3]
        r2=routing[4]
        r3=routing[5]
        if gf.euDis(tup,c1)<r1 and gf.euDis(tup,c2)<r2 and gf.euDis(tup,c1)>r3:
            return True
        return False
    
    
    def changeOffset(self,num):
        if self.msgRes and len(self.msgRes)!=0:
        
            self.messageIndex+=num
            self.messageIndex=self.messageIndex%len(self.msgRes)
            if self.messageIndex<0:
                self.messageIndex=len(self.msgRes)-1
            self.messageLabel.config(text=str(self.msgRes[self.messageIndex]))
            self.current_button.config(text=str(self.messageIndex))
            
            
            
    def demoArea(self):
        routing=self.msgRes[self.messageIndex]
        if self.msgFlag and len(self.msgFlag)>self.messageIndex and self.msgFlag[self.messageIndex]==0:
            if len(routing)>14:
                buf=[]
                for ele in self.anyHyperbola(self.WSN.getMote(int(routing[1])).getLocTup(),self.WSN.getMote(int(routing[2])).getLocTup(),routing[4]):
                    buf.append(ele)
                
                for ele in self.anyHyperbola(self.WSN.getMote(int(routing[1])).getLocTup(),self.WSN.getMote(int(routing[2])).getLocTup(),routing[5]):
                    buf.append(ele)
                buf.append(self.anyCycle(  self.WSN.getMote(int(routing[3])).getLocTup(),int(routing[6]) ) )
                
                self.eleDic[self.messageIndex]=buf
                
            else:
                buf=[]
                buf.append(self.anyCycle(  self.WSN.getMote(int(routing[1])).getLocTup(),int(routing[3]) ))
                buf.append(self.anyCycle(  self.WSN.getMote(int(routing[2])).getLocTup(),int(routing[4]) ) )
                buf.append(self.anyCycle(  self.WSN.getMote(int(routing[1])).getLocTup(),int(routing[5]) ))
                
                self.eleDic[self.messageIndex]=buf
                
            self.msgFlag[self.messageIndex]=1
        elif self.msgFlag and len(self.msgFlag)>self.messageIndex and self.msgFlag[self.messageIndex]==1:
            for ele in self.eleDic[self.messageIndex]:
                self.c.delete(ele)
            self.msgFlag[self.messageIndex]=0
            
            
        return           


    
    
    
    
    
    def create_window(self):
        if self.Cbutton['state']==DISABLED:
            return
        self.Cbutton['state']=DISABLED
        self.counter += 1
        self.t = Toplevel(self.root)
        
        self.t.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.t.wm_title("Wireless sensor network setting")
        lable_node_number = Label(self.t, text="Choose number of nodes in the network" ,font=self.helv16)
        lable_node_number.grid(row=0, column=0)
        self.choose_node_number = Scale(self.t, from_=100, to=5000, orient=HORIZONTAL,variable=self.default_node_number)
        self.choose_node_number.set(self.default_node_number)
        self.choose_node_number.grid(row=0, column=1)
        
        lable_anchor_number = Label(self.t, text="Choose number of anchors in the network" ,font=self.helv16)
        lable_anchor_number.grid(row=1, column=0)
        self.choose_anchor_number = Scale(self.t, from_=3, to=200, orient=HORIZONTAL,variable=self.default_anchor_number)
        self.choose_anchor_number.set(self.default_anchor_number)
        self.choose_anchor_number.grid(row=1, column=1)
        
        lable_radio_range = Label(self.t, text="Choose the sensor radio range" ,font=self.helv16)
        lable_radio_range.grid(row=2, column=0)
        self.choose_radio_range = Scale(self.t, from_=10, to=200, orient=HORIZONTAL,variable=self.default_radio_range)
        self.choose_radio_range.set(self.default_radio_range)
        self.choose_radio_range.grid(row=2, column=1)
        
        lable_width = Label(self.t, text="Choose the width of the sensor field" ,font=self.helv16)
        lable_width.grid(row=3, column=0)
        self.choose_width = Scale(self.t, from_=500, to=5000, orient=HORIZONTAL,variable=self.default_width)
        self.choose_width.set(self.default_width)
        self.choose_width.grid(row=3, column=1)
        
        lable_length = Label(self.t, text="Choose the length of the sensor field" ,font=self.helv16)
        lable_length.grid(row=4, column=0)
        self.choose_length = Scale(self.t, from_=500, to=5000, orient=HORIZONTAL,variable=self.default_length)
        self.choose_length.set(self.default_length)
        self.choose_length.grid(row=4, column=1)
        
        confirm_button = Button(self.t,text='confirm', command=self.generateWSNs,font=self.helv36)
        confirm_button.grid(row=5,column=0)
        
        cancel_button = Button(self.t,text='cancel', command=self.on_closing,font=self.helv36)
        cancel_button.grid(row=5,column=1)
        
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        w = 600
        h = 300
        yoff= min(400,max(0,1000-h))
        self.t.geometry("%dx%d+%d+%d" % (w, h, x + self.default_width/2,yoff))
        

    def debug(self):
        offsetX=self.offsetX+200
        offsetY=self.offsetY+200

        centerWidth=self.canvasWidth/2
        centerLength=self.canvasHeight/2
        r1=self.default_radio_range
        r=self.default_radio_range
        radius=centerLength-offsetY+self.default_radio_range/3
        self.c.create_oval(self.canvasWidth/2-radius,self.canvasHeight/2-radius,self.canvasWidth/2+radius,self.canvasHeight/2+radius)
        
        while (r1<centerWidth-offsetX or r1<centerLength-offsetY):
            
            
            self.c.create_oval(centerWidth-r1, centerLength-r1, centerWidth+r1, centerLength+r1,
                                   width=self.default_radio_range, outlinestipple="gray12")
            self.draw1.ellipse([centerWidth-r1, centerLength-r1, centerWidth+r1, centerLength+r1],outline='black')                       
            r1+=2*r
            
        self.c.create_line(centerWidth, centerLength-1.5*self.default_radio_range, centerWidth, 
                           centerLength-r1+2*r,width=self.default_radio_range,
                           capstyle=ROUND, smooth=TRUE,stipple="gray12")  
        self.draw1.line([centerWidth, centerLength-1.5*self.default_radio_range, centerWidth, 
                           centerLength-r1+2*r],fill='black')                  
        self.c.create_line(centerWidth, centerLength+1.5*self.default_radio_range, centerWidth, 
                           centerLength+r1-2*r,width=self.default_radio_range,
                           capstyle=ROUND, smooth=TRUE,stipple="gray12")
        self.draw1.line([centerWidth, centerLength+1.5*self.default_radio_range, centerWidth, 
                           centerLength+r1-2*r],fill='black')
        image2=self.image1.crop((centerWidth-offsetX-100,centerLength-offsetY-300,centerWidth+offsetX+100,centerLength+offsetY+300))
        image2.thumbnail((64,64))
        currentDT = datetime.datetime.now()
        image2.save(str(currentDT.hour)+str(currentDT.minute)+str(currentDT.second)+".jpg")                   
                           
        for x in range(0,self.canvasWidth):
            for y in range(0,self.canvasHeight):
                dis=gf.euDis((centerWidth,centerLength),(x,y))
                if int(round(dis/self.default_radio_range))%2==1 and dis<=r1-r:
                    self.routingAreaSet.add((x,y))
                    
                if x<centerWidth+self.default_radio_range/2 and x>centerWidth-self.default_radio_range/2 and y < centerLength-self.default_radio_range and y> centerLength-r1+2*r:
                    self.routingAreaSet.add((x,y))
                    
                if x<centerWidth+self.default_radio_range/2 and x>centerWidth-self.default_radio_range/2 and y > centerLength+self.default_radio_range and y< centerLength+r1-2*r:
                    self.routingAreaSet.add((x,y))
                    
        '''            
        for tup in self.routingAreaSet:

            self.anyCycle(tup,1) 
        '''
                                                
        return    
            
    def on_closing(self):
        self.Cbutton['state']='normal'
        self.t.destroy()
    def on_closingS(self):
        self.Sbutton['state']='normal'
        self.t.destroy()
        
    def generateWSNs(self):
        self.clearAll()
        self.WSN=[]
        gc.collect()
        self.default_node_number=self.choose_node_number.get()
        self.default_anchor_number=self.choose_anchor_number.get()
        self.default_width=self.choose_width.get()
        self.default_length=self.choose_length.get()
        self.default_radio_range=self.choose_radio_range.get()
        if self.default_width<self.canvasWidth-40:
            x1=(self.canvasWidth-self.default_width)/2
            x2=(self.canvasWidth+self.default_width)/2
        else:
            x1=20
            x2=self.default_width+20
        if self.default_length <self.canvasHeight -20 :
            y1=(self.canvasHeight-self.default_length)/2
            y2=(self.canvasHeight+self.default_length)/2
        else:
            y1=10
            y2=self.default_length+10

        self.WSN=WSNs(self.default_node_number, self.default_anchor_number,self.default_radio_range,x1,y1,x2,y2)
        self.offsetX=x1
        self.offsetY=y1
        
        gc.collect()
        
        for M in self.WSN.moteList:
            
            cord=[M.x, M.y]
            if M.isAnchor:
                self.nodeDic[M.ID]=self.c.create_circle(cord[0],cord[1],self.moteSize*2,fill='red')
            else:
                self.nodeDic[M.ID]=self.c.create_circle(cord[0],cord[1],self.moteSize,fill='black')
                
       
        self.c.config(scrollregion = self.c.bbox("all"))
        gc.collect()
        self.on_closing()


    def use_pen(self):
        self.activate_button(self.pen_button)

    def use_brush(self):
        self.activate_button(self.brush_button)

    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]

    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)
    
    def clearAll(self):
        self.B=[]
        self.C=[]
        self.setToShowed=set()
        self.messageArea=dict()
        self.priorityCoverage=[]
        self.messageButtonList=[]
        self.step1Results=[]
        self.WSN=[]
        self.trace=[]
        self.nodeHopVector=[]
        self.nodeDic=dict()
        self.routingArea=[]
        self.routingAreaSet=set()
        self.c.delete("all")
        gc.collect()
        
    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def paint(self, event):
        if self.active_button==self.pen_button:
            self.line_width = self.choose_size_button.get()
            self.trace.append((event.x,event.y))
            paint_color = 'white' if self.eraser_on else self.color
            if self.old_x and self.old_y and (self.old_x!=event.x or self.old_y!=event.y):
                self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                                   width=self.line_width, fill=paint_color,
                                   capstyle=ROUND, smooth=TRUE, splinesteps=36, stipple="gray12")
                self.draw1.line([self.old_x, self.old_y, event.x, event.y], fill='black')                  
            self.addToRoutingArea(event.x,event.y,self.line_width/2)

            self.old_x = event.x
            self.old_y = event.y
    
    
    
    def addToRoutingArea(self,x,y,w):
    
        for a in range(x-w,x+w):
            for b in range(y-w,y+w):
                if (x-a)**2+(y-b)**2<w**2:
                    self.routingAreaSet.add((a,b))  

    def bestLocation(self, cID):
        tup=self.c.coords(self.nodeDic[cID])
        x=0
        y=0
        
        if tup[0]<self.default_width-200*(1+(self.WSN.anchorNum-1)/20)-50:
            x=tup[0]+50
        else:
            #x=tup[0]-50-200*(1+(self.WSN.anchorNum-1)/30)
            x=100
        if tup[1]<self.default_length-400:
            y=tup[1]
        else:
            y=self.default_length-550
        return (x,y)

    def reset(self, event):
        self.old_x, self.old_y = None, None
        
        if self.active_button==self.brush_button:
            self.clickNode(self.findCloseNode(event.x,event.y))
            
        if self.final_msg and self.active_button==self.simulate_button:
            curNode=self.findCloseNode(event.x,event.y)
            if curNode!=-1:
                self.simulateFrom(curNode,self.final_msg)
        
        
    def simulateFrom(self,startingNode, msg):
       
        print "good through now"
        print "Starting from node:"+str(startingNode)
        
        
        os.system("./simulation/runSim.sh " +str(startingNode)+" "+str(msg).replace(" ",""))
        
        
        
        
        
        
        
        
        

    def clickNode(self,clickedNode):
        if self.old_node!=-1:
            if self.old_node in self.nodeDic:
                for cID in self.nodeHopVector:
                    self.c.delete(cID)
                self.nodeHopVector=[]
            self.old_node = -1
        else:
            self.old_node=clickedNode
            #print 'event X: '+str(event.x) + ' event Y ' + str(event.y)+ ' node '+str(self.old_node)
            
            if self.old_node !=-1:
                paper=self.bestLocation(self.old_node)
                tup=self.c.coords(self.nodeDic[self.old_node])
                self.nodeHopVector.append(self.c.create_rectangle(paper[0], paper[1], paper[0]+200*(1+(self.WSN.anchorNum-1)/30), paper[1]+620,fill='white'))
                self.nodeHopVector.append(self.c.create_text(paper[0]+100*(1+(self.WSN.anchorNum-1)/30),paper[1]+10,text='Node ID:'+ str(self.old_node)+',x:' + str((tup[0]+tup[2])/2)+'  y:'+str((tup[1]+tup[3])/2)))
                if self.WSN.findNode(self.old_node):
                    iii=0
                    for key in self.WSN.findNode(self.old_node).hop:
                        
                        hh=self.WSN.findNode(self.old_node).hop[key]
                        self.nodeHopVector.append(self.c.create_text(paper[0]+100+200*(iii/30),paper[1]+20*(1.5+iii%30),text='Anchor: '+str(key)+'; Hops: '+str(hh)))
                        iii+=1

    def findCloseNode(self,x,y):
        for key in self.nodeDic:
            tup=self.c.coords(self.nodeDic[key])
            if tup[0]<=x+2 and tup[1]<=y+2 and tup[2]>=x-2 and tup[3]>=y-2:
                return key
        
        return -1
        

if __name__ == '__main__':
    sys.stdout.flush() 
    pt=Paint()
