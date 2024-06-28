import time

# peer
# regardless the launching sequence, the execution will activate in turn
# peer 1 then 2 and then 3, repeating

def main():

  peerNum = 1
  numOfPeers=3
  sleepTime=0.1

  # if channels - In & Ou - have value "0", the program runs alone
  channelIn="3"
  channelOu="1"
  if channelIn!="0" or channelOu !="0":
    import redis
    rd = redis.client.StrictRedis()


  N=10
  K=10

 


    
  countingFrom=1

  if channelIn != "0":
   sub1 = rd.pubsub()
   try:
     sub1.subscribe(channelIn) # you can have sub2, sub3, ...
   except:
     print "Error: regis is not running"
     return

   # subscribing generates a message via the channel to all the subscribers
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
     if   (countingFrom==1 and peerNum==1): pass
     elif channelIn == "0":                 pass
     else:
       s=sub1.listen().next() # the content is not relevant being the channel
                              # used only to broadcast a message to unlock a
                              # step


       
       # get variables from the redis space via redis
       # recovering them in a sincronized way

       greetings=rd.get("greetings") #greetings contains a string    
       if greetings == None: print "something went wrong in peer "+str(peerNum)+\
                                   "; impossible to get a content for 'greetings' var"
       else: print "got 'greetings' variable from memory space, with content "+\
             greetings

       countingFrom=rd.get("countingFrom")
       # if the value has been published by the peer using R and redis, the
       # format is a string, so we have to convert it (in case, using int(float(...
       if type(countingFrom) is str: countingFrom=int(float(countingFrom))
       if countingFrom == None: print "something went wrong in peer "+str(peerNum)+\
                                   "; impossible to get a content for 'contingFrom' var"
       else: print "got 'countingFrom' variable from memory space, with content "+\
             str(countingFrom)

 
     

     # *******************************
     # here this peer is doing its job
     for i in range(countingFrom,countingFrom+K):
       print "peer # "+str(peerNum)+" writing "+str(i)
     # *******************************

     countingFrom+=K

     
     # set variables in redis space,
     # to recover them in a sincronized way from another peer

     if channelOu != "0":
      rd.set("greetings","Hello "+str(countingFrom))
      print "peer "+str(peerNum)+" set 'greetings' variable in redis memory space"

     
      rd.set("countingFrom",countingFrom)
      print "peer "+str(peerNum)+" set 'countingFrom' variable in redis memory space"
     

      # passing the execution to another peer, repeating if the receiver is not
      # listening
      if countingFrom < N*K*numOfPeers+1: # not all tasks finished
        num=0
        while num != 1:
          num=rd.publish(channelOu,'OK') # the content of the message is not relevant
          if num != 1:
           print "Error: listener missing on channel "+channelOu+"; retrying ..."
           time.sleep(sleepTime)

        print "published 'OK' on channel "+channelOu



  print "Peer "+str(peerNum)+" finishing."

 
if __name__ == '__main__':
  main()
