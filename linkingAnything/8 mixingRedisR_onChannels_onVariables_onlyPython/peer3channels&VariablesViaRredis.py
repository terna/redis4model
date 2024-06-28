# emulating NetLogo situation
###
### externally, activate R with
### library(Rserve)
### Rserve()          |  in MacOS: Rserve(args="--no-save")

### if the library is missing
### install.packages("Rserve")

import pyRserve
import time
import random

# peer
# regardless the launching sequence, the execution will activate in turn
# peer 1 then 2 and then 3, repeating

def main():

  peerNum = 3
  channelIn="2"
  channelOu="3"

  N=10
  numOfPeers=3
  K=10

  # activating redis in R
  cRr=pyRserve.connect(host="localhost")
  cRr.r('library(rredis)')
  cRr.r('redisConnect()')


    
  countingFrom=1
    
  # considering the code of peers 1 and 2:
  # please note that here is not necessary to execute an empty listening
  # operation to clean the channel from the reaction to subscription
  
  for n in range(N):

     # receiving execution from another peer, but the case of the first
     # step of peer 1
     if (countingFrom==1 and peerNum==1):
       pass
     else:
       cRr.r('redisSubscribe("'+channelIn+'")')
       print "channel "+channelIn+" subscribed" 

       s=cRr.r('redisMonitorChannels()')

       # the received message is not relevant; simply a message via the channels
       # unlocks the peer

       #print s # uncomment to se all the elements coming form the channel
       cRr.r('redisUnsubscribe("'+channelIn+'")')
       print "unsubscribed channel "+channelIn



       
       # get variables from the redis space via rredis
       # recovering them in a sincronized way
       greetings=cRr.r('redisGet("greetings")')
       if greetings == None: print "something went wrong in peer "+str(peerNum)+\
                                   "; impossible to get a content for 'greetings' var"
       else: print "got 'greetings' variable from memory space, with content "+\
             greetings
       

       countingFrom=cRr.r('redisGet("countingFrom")')
       if countingFrom == None: print "something went wrong in peer "+str(peerNum)+\
                                   "; impossible to get a content for 'countingFrom' var"
       else: print "got 'countingFrom' variable from memory space, with content "+\
             str(countingFrom)
       # countingFrom world be an int, coming from the other peers, but redisGet
       # imports it as a str
       countingFrom=int(countingFrom)


 
     

     # *******************************
     # here this peer is doing its job
     for i in range(countingFrom,countingFrom+K):
       print "peer # "+str(peerNum)+" writing "+str(i)
     # *******************************

     countingFrom+=10

     
     # as a feasibility test, set variables in redis space via rredis,
     # to recover them in a sincronized way from another peer
     cRr.r.var="Hello "+str(countingFrom)
     cRr.r('txt=toString(var)')
     # only strings and sent in raw way to redis
     cRr.r('redisSet("greetings", charToRaw(txt))')
     print "peer "+str(peerNum)+" set 'greetings' variable in redis memory space"

     cRr.r.var=countingFrom
     cRr.r('txt=toString(var)')
     # only strings and sent in raw way to redis
     cRr.r('redisSet("countingFrom", charToRaw(txt))')
     print "peer "+str(peerNum)+" set 'countingFrom' variable in redis memory space"
     

     # passing the execution to another peer (the content is unimportant)
     if countingFrom < N*K*numOfPeers+1: # not all tasks finished
       num=0
       while num != 1:
         num=cRr.r('redisPublish("'+channelOu+'","OK")')
         if num != 1:
          print "Error: listener missing on channel "+channelOu+"; retrying ..."
          time.sleep(0.1)

       print "published on channel "+channelOu



  print "Peer "+str(peerNum)+" finishing."

 
if __name__ == '__main__':
  main()
