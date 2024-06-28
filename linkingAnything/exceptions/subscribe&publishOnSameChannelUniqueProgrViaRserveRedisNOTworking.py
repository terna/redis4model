import pyRserve
 
def interact():

  cn=pyRserve.connect(host="localhost")
  cn.r('library(rredis)')
  cn.r('redisConnect()')


  chn='ch1'

  x=42
  num=cn.r('redisPublish("'+chn+'",'+str(x)+')')
  print num
  print "here1"

  cn.r('redisSubscribe("'+chn+'")')
  print "here2"

  #print cn.r('redisMonitorChannels()')

  num=cn.r('redisPublish("'+chn+'",'+str(x)+')')
  print num
   
  print cn.r('redisMonitorChannels()')

  

if __name__ == '__main__':
	  interact()

"""
in R

library(Rserve)
Rserve(args="--no-save") || Rserve() if not MacOS

"""
