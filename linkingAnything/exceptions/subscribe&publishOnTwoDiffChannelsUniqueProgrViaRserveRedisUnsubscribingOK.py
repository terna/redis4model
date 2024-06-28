import pyRserve
 
def interact():

  cn=pyRserve.connect(host="localhost")
  cn.r('library(rredis)')
  cn.r('redisConnect()')


  chn1='ch1'
  chn2='ch2'

  x=42
  num=cn.r('redisPublish("'+chn1+'",'+str(x)+')')
  print num
  print "here1"

  cn.r('redisSubscribe("'+chn2+'")')
  print "here2"

  #print cn.r('redisMonitorChannels()')

  cn.r('redisUnsubscribe("'+chn2+'")')
  print "here3"
  

  num=cn.r('redisPublish("'+chn1+'",'+str(x)+')')
  print num
  print "here4"
   
  #print cn.r('redisMonitorChannels()')

  

if __name__ == '__main__':
	  interact()

"""
in R

library(Rserve)
Rserve(args="--no-save") || Rserve() if not MacOS

"""
