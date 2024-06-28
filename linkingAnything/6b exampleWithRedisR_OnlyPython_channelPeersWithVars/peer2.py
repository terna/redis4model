import pyRserve
import time

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

  cn=pyRserve.connect(host="localhost")
  cn.r('library(rredis)')
  cn.r('redisConnect()')


    
  countingFrom=1
    
  # camparizon with 5 folder: is not necessary here to execute an empty listen
  # operation to clean the channel form the reaction to subscription
  
  for n in range(N):

     # receiving execution from another peer, but the case of the first
     # step of peer 1
     if (countingFrom==1 and peerNum==1):
       # flushing redis space and continuing
       cn.r('redisFlushAll()')
       pass
     else:
       cn.r('redisSubscribe("'+channelIn+'")')
       print "subscribed channel "+channelIn 

       s=cn.r('redisMonitorChannels()')

       countingFrom = int(s[-1]) # [-1] means: the last element
       #print s # uncomment to se all the elements coming form the channel
       cn.r('redisUnsubscribe("'+channelIn+'")')
       print "unsubscribed channel "+channelIn

       
       # as a feasibility test, get a variable from the redis space via rredis
       # recovering it in a sincronized way
       greetings=cn.r('redisGet("greetings")')
       if greetings == None: print "something went wrong in peer "+str(peerNum)+\
                                   "; impossible to get a content for 'greetings' var"
       else: print "got 'greetings' variable from memory space, with content "+\
             greetings
       

 
     

     # ******************************
     # here this peer is doing it job
     for i in range(countingFrom,countingFrom+K):
       print "peer # "+str(peerNum)+" writing "+str(i)
     # ******************************

     countingFrom+=10

     
     # as a feasibility test, set a variable in redis space via rredis and
     # to recover it in a sincronized way from another peer
     cn.r('redisSet("greetings","Hello '+str(int(countingFrom))+'")')
     print "peer "+str(peerNum)+" set 'greetings' variable in memory space"
     

     # passing the execution to another peer (sending countingFrom value;
     # if necessary, the argument can a more complex object, e.g. a quoted list
     # of values to be splitted by the receiver)
     if countingFrom < N*K*numOfPeers+1: # not all tasks finished
       num=0
       while num != 1:
         num=cn.r('redisPublish("'+channelOu+'",'+str(countingFrom)+')')
         print "published on channel "+channelOu
         if num != 1:
          print "Error: listener missing on channel "+channelOu+"; retrying ..."
          time.sleep(0.1)




  print "Peer "+str(peerNum)+" finishing."

 
if __name__ == '__main__':
  main()
