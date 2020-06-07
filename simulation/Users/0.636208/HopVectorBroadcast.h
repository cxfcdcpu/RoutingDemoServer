#ifndef TWO_NODES_H
#define TWO_NODES_H


typedef nx_struct request_msg{
  nx_uint8_t mode;
  nx_uint32_t requestID;
  nx_uint8_t dataSize;
  nx_uint8_t routingMessage[108];
}request_msg_t;


enum {
  AM_REQUEST_MSG = 6,
  AM_HopVector = 6,
  REQUEST_QUEUE_LEN=32,
  COUNTER_THRESHOLD=5,
  REQUEST_GROUP = 6
};

#endif
