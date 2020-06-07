#include "Timer.h"
#include "HopVectorBroadcast.h"
#include "Neighbor.h"
#include "hopVector.h"
#include "universal_functions_new.h"

module HopVectorBroadcastC @safe() {
  uses {
    interface Boot;
    interface Receive as RequestReceive;
    
    interface AMSend as RequestSend;

    interface AMPacket as RadioAMPacket;
    interface Timer<TMilli> as wait1;
    interface LocalTime<TMilli> as LocalT;
    interface SplitControl as AMControl;
  }
}
implementation {

  message_t requestPacketsBuf[REQUEST_QUEUE_LEN];
  message_t  * ONE_NOK requestPackets[REQUEST_QUEUE_LEN];
  
  
  
  uint8_t requestIndex=0;
  
  uint16_t seed=10;
  bool receiveLock=FALSE;
  request_msg_t localRequest;
  uint32_t requestStartTime;
  uint32_t requestCurrentTime;
  uint8_t myIndex=0;

  
  uint16_t Tback=2000;
  uint16_t TB=2500;
  uint8_t backThreshold=COUNTER_THRESHOLD;
  uint32_t buf=0;
  
  
  bool locked=FALSE;
  bool flag=FALSE;
  bool flag2=FALSE;
  
  uint8_t starter =2;
  uint8_t jumper = 2;
  
  uint32_t i;
  uint32_t j;
  
  uint16_t countNeighbor = 1;
  uint32_t currentT;
  uint32_t timeSpan = 0;
  uint16_t total =0;
  
  
  uint32_t requestList[32]={2147483647,2147483647,2147483647,2147483647,
                            2147483647,2147483647,2147483647,2147483647,
                            2147483647,2147483647,2147483647,2147483647,
                            2147483647,2147483647,2147483647,2147483647,
                            2147483647,2147483647,2147483647,2147483647,
                            2147483647,2147483647,2147483647,2147483647,
                            2147483647,2147483647,2147483647,2147483647,
                            2147483647,2147483647,2147483647,2147483647};
                            
  uint8_t requestBackList[32]={255, 255, 255, 255, 255, 255, 255, 255,  
                                255, 255, 255, 255, 255, 255, 255, 255, 
                                255, 255, 255, 255, 255, 255, 255, 255, 
                                255, 255, 255, 255, 255, 255, 255, 255};
                                
                          
  
  uint16_t arr[60]={65535,65535,65535,65535,65535,65535,65535,65535,65535,65535,
                    65535,65535,65535,65535,65535,65535,65535,65535,65535,65535,
                    65535,65535,65535,65535,65535,65535,65535,65535,65535,65535,
                    65535,65535,65535,65535,65535,65535,65535,65535,65535,65535,
                    65535,65535,65535,65535,65535,65535,65535,65535,65535,65535,
                    65535,65535,65535,65535,65535,65535,65535,65535,65535,65535};
  uint8_t id[240]={255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255};
  uint8_t hop[240]={255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255,
                   255,255,255,255,255,255,255,255,255,255};
                   

  uint16_t *pArr = arr;
  uint8_t *pID = id;
  uint8_t *pHop = hop;
  uint8_t sendingMode;
  task void requestSend();
  
  event void Boot.booted(){
   atomic
   {
    seed=TOS_NODE_ID;
    getNeighbor(pArr);
    getHopVector(pID,pHop);
    
    for (i = 0; i < REQUEST_QUEUE_LEN; i++)
      requestPackets[i] = &requestPacketsBuf[i];
    
    for(j=0;j<60;j++)
    {
      if(pArr[j]<65535)
      {
        countNeighbor+=1;
      }
    }
    
    seed=countNeighbor*seed;
   } 
    call AMControl.start();
  }



  event void AMControl.startDone(error_t err) {

    if (err == SUCCESS) {


        locked = FALSE;

    }
    else {
      call AMControl.start();
    }
  }


  event void AMControl.stopDone(error_t error){}
  
  event message_t *RequestReceive.receive(message_t *msg, void *payload, uint8_t len){
    am_id_t amID;
    uint32_t ID;
    request_msg_t *rmsg;
    uint8_t ds;
    uint8_t* ret;
    uint16_t randTime;
    uint8_t jump;
    uint8_t curI;
    
    amID=call RadioAMPacket.type(msg);
    
    //if(amID==REQUEST_GROUP)
    //{
      rmsg=payload;
      ret=payload;
      ID=rmsg->requestID;
      ds=rmsg->dataSize;
      flag=TRUE;
      myIndex=0;
      for( i=0;i<REQUEST_QUEUE_LEN;i++)
      {
        if(requestList[i]==ID)
        {
          flag=FALSE;
          myIndex=i;
        }
        
      
      }
      atomic
     { 
      
      if(flag)
      {
        timeSpan = call LocalT.get();
        dbg("LocalTime", "000, %hu ,timeSpan: %lu \n",TOS_NODE_ID,timeSpan);
        requestPackets[requestIndex] = msg;
        requestList[requestIndex]=ID;
        requestBackList[requestIndex]=0;
        requestIndex = (requestIndex+1)%REQUEST_QUEUE_LEN;
         seed=randS(seed);
         randTime=seed%10+1;
        //call wait1.startOneShot(TB*randTime/countNeighbor);
      
       }
       else
       {
         requestBackList[myIndex]+=1;
         if (requestBackList[myIndex]>backThreshold)requestBackList[myIndex]-=1;
         seed=randS(seed);
         randTime=seed%10+1;
         call wait1.stop();
         //call wait1.startOneShot(Tback*randTime/countNeighbor);
       
       }
       
       curI=6;
       jump=5;
       flag2=FALSE;
       
       while(ret[curI]!=255)
       {
         //dbg("LocalTime", "222, [%hu, %hu, %hu, %hu, %hu]\n", ret[curI],ret[curI+1],ret[curI+2],ret[curI+3],ret[curI+4]);
         //dbg("LocalTime", "444, [%hu, %hu, %hu]\n", pHop[ret[curI]],pHop[ret[curI+1]],pHop[ret[curI+2]]);
         if((pHop[ret[curI]]-pHop[ret[curI+1]]==2*ret[curI+3]-1||pHop[ret[curI]]-pHop[ret[curI+1]]==2*ret[curI+3]-2)&&pHop[ret[curI+2]]<=ret[curI+4])
            flag2=TRUE;
         curI+=jump;
       }
       curI+=1;
       jump=4;
       while(curI<ds+6)
       {
         if((pHop[ret[curI]]==ret[curI+2]) && pHop[ret[curI+1]]<=ret[curI+3])
           flag2=TRUE;
       
         curI+=jump;
       }
       
       if (flag2)
       {
         //dbg("LocalTime", "333, time: %hu \n", Tback*randTime/countNeighbor);
         call wait1.startOneShot(Tback*randTime/countNeighbor);
       
       }
       
       
      }
    //}
    return msg;
  } 




  
  task void requestSend(){


  }
  


  event void wait1.fired() {
    message_t* smsg;
    
    //dbg("LocalTime", "555, %hu ,time: %hu \n", TOS_NODE_ID,requestBackList[myIndex]);
    if( requestBackList[myIndex]<backThreshold)
    {
      smsg=requestPackets[myIndex];

      if(!locked){
        if(call RequestSend.send(AM_BROADCAST_ADDR, smsg, sizeof (request_msg_t)) == SUCCESS)
            locked = TRUE;
      }
    }
  }



  event void RequestSend.sendDone(message_t* bufPtr, error_t error) {
    timeSpan = call LocalT.get();
    total++;
    locked = FALSE;
    requestBackList[myIndex]=155;
    dbg("LocalTime", "111, %hu ,timeSpan: %lu\n",TOS_NODE_ID,timeSpan);

  }
  


}
