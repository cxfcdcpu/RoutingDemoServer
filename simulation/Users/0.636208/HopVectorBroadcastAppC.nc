#include "HopVectorBroadcast.h"

configuration HopVectorBroadcastAppC {}
implementation {
  components MainC, HopVectorBroadcastC as App, ActiveMessageC;
  components new AMSenderC(REQUEST_GROUP) as requestSender;
  components new AMReceiverC(REQUEST_GROUP) as requestReceiver; 
  
  components new TimerMilliC() as Wait1;
  components LocalTimeMilliC as localT;
  App.Boot -> MainC.Boot;
  
  App.RequestReceive -> requestReceiver;
  App.RequestSend -> requestSender;
  
  App.AMControl -> ActiveMessageC;
  App.RadioAMPacket ->ActiveMessageC;
  

  App.wait1 -> Wait1;
  App.LocalT -> localT;
}
