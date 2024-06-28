#From different terminals you can launch several running instances of slave.py

import redis
 
def interact():
  r = redis.client.StrictRedis()
  sub1 = r.pubsub()
  sub1.subscribe('chX1')
  s=sub1.listen().next() #receives the subscribe message as a dictionary
  if s["type"] != "subscribe":
    print "subscription error to a channel"
    exit(1)
  #successive listen().next() will return a "message" value for 'type' key

  print "subscribed"

  raw_input("Enter to start listening")
  
  print "listening"
  
  """
  x1x1=sub1.listen().next()
  x1=x1x1['data']
  print x1
  """
  for x1x1 in sub1.listen():
    x1=x1x1['data']
    print x1
    if int(x1)==0:
      print "Now stopping"
      return



if __name__ == '__main__':
	  interact()
