COMPONENT=HopVectorBroadcastAppC
BUILD_EXTRA_DEPS = requestMsg.py


CFLAGS += -DTOSH_DATA_LENGTH=114
CFLAGS += -DCC2420_NO_ACKNOWLEDGEMENTS
CFLAGS += -DCC2420_DEF_CHANNEL=11
CFLAGS += -DCC2420_DEF_RFPOWER=31
CFLAGS += -DPOWERTOSSIMZ


requestMsg.py: HopVectorBroadcast.h
	mig python -target=$(PLATFORM) $(CFLAGS) -python-classname=requestMsg HopVectorBroadcast.h request_msg  -o $@
    
include $(MAKERULES)

