import redis
import time
import pyRserve

# peer
# regardless the launching sequence, the execution will activate in turn
# peer 1 then 2 and then 3, repeating

def main():

  peerNum = 2
  channelIn="1"
  channelOu="2"

  N=10
  numOfPeers=3
  K=10

  rd = redis.client.StrictRedis()

  # here we create a connection to an R server, that will be used only to
  # get/set in redis memory space
  cRr=pyRserve.connect(host="localhost")
  cRr.r('library(rredis)')
  cRr.r('redisConnect()')


    
  countingFrom=1

  sub1 = rd.pubsub()
  try:
    sub1.subscribe(channelIn) # you can have sub2, sub3, ...
  except:
    print "Error: regis is not running"
    return

  # subscribing generate a message via the channel to all the subscribers
  # here each channel has a unique subscriber
  s=sub1.listen().next() #receives the subscribe message as a dictionary
  if s["type"] == "subscribe":
    print "channel "+channelIn+" subscribed"
  else:
    print "subscription error (channel "+channelIn+")"
    return
   

    
  
  for n in range(N):

     # receiving execution from another peer, but the case of the first
     # step of peer 1
     if (countingFrom==1 and peerNum==1): pass
     else:
       s=sub1.listen().next() # the content is not relevant being the channel
                              # used only to broadcast a meesage to unlock a
                              # step


       
       # get variables from the redis space via R & redis
       # recovering it in a sincronized way

       cRr.r('greetings=redisGet("greetings")')
       #greetings=cRr.r('greetings')
       greetings=cRr.r.greetings
      
       if greetings == None: print "something went wrong in peer "+str(peerNum)+\
                                   "; impossible to get a content for 'greetings' var"
       else: print "got 'greetings' variable from memory space, with content "+\
             greetings


       cRr.r('countingFrom=redisGet("countingFrom")')
       countingFrom=cRr.r.countingFrom                             
       if countingFrom == None: print "something went wrong in peer "+str(peerNum)+\
                                   "; impossible to get a content for 'contingFrom' var"
       else: print "got 'countingFrom' variable from memory space, with content "+\
             str(countingFrom)

 
     

     # *******************************
     # here this peer is doing its job
     for i in range(countingFrom,countingFrom+K):
       print "peer # "+str(peerNum)+" writing "+str(i)
     # *******************************

     countingFrom+=10

     
     # set variables in redis space via rredis,
     # to recover them in a sincronized way from another peer
     
     #cRr.r('greetings="Hello '+str(countingFrom)+'"')
     cRr.r.greetings="Hello "+str(countingFrom)
     cRr.r('redisSet("greetings",greetings)')
     print "peer "+str(peerNum)+" set 'greetings' variable in redis memory space"

     
     cRr.r.countingFrom=countingFrom
     cRr.r('redisSet("countingFrom",countingFrom)')
     print "peer "+str(peerNum)+" set 'countingFrom' variable in redis memory space"
     

     # passing the execution to another peer, repeating if the receiver is not
     # listening
     if countingFrom < N*K*numOfPeers+1: # not all tasks finished
       num=0
       while num != 1:
         num=rd.publish(channelOu,'OK') # the content of the message is not relevant
         if num != 1:
          print "Error: listener missing on channel "+channelOu+"; retrying ..."
          time.sleep(0.1)

       print "published OK on channel "+channelOu



  print "Peer "+str(peerNum)+" finishing."

 
if __name__ == '__main__':
  main()
