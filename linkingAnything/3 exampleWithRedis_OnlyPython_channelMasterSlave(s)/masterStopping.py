import redis

 
def main():

  chn="chX1"
  
  r = redis.client.StrictRedis()

  num=r.publish(chn, 0) # to stop clients
  print "Published on channel "+chn+" with "+str(num)+" listener/s"
 
if __name__ == '__main__':
  main()
