import redis
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
  
  r = redis.client.StrictRedis()

  sub1 = r.pubsub()
  try:
    sub1.subscribe(channelIn) # you can have sub2, sub3, ...
  except:
    print "Error: regis is not running"
    return

  
  countingFrom=1
    
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
     else: countingFrom = int(sub1.listen().next()["data"])
 
     

     # ******************************
     # here this peer is doing it job
     for i in range(countingFrom,countingFrom+K):
       print "peer # "+str(peerNum)+" writing "+str(i)
     # ******************************

     countingFrom+=10


     # passing the execution to another peer (sending countingFrom value;
     # if necessary, the argument can a more complex object, e.g. a quoted list
     # of values to be splitted by the receiver)
     if countingFrom < N*K*numOfPeers+1: # not all tasks finished
       num=0
       while num != 1:
         num=r.publish(channelOu, countingFrom)
         if num != 1:
          print "Error: listener missing on channel "+channelOu+"; retrying ..."
          time.sleep(0.1)



  print "Peer "+str(peerNum)+" finishing."

 
if __name__ == '__main__':
  main()
