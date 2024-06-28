#From different terminals you can launch several running instances of slave.py

import pyRserve
 
def interact():

  cn=pyRserve.connect(host="localhost")
  cn.r('library(rredis)')
  cn.r('redisConnect()')

  cn.r('redisSubscribe("ch1")')

  print "subscribed to 'ch1'"
  
  s=cn.r('redisMonitorChannels()')
  print s
  print s[-1]

  """
    for x1x1 in sub1.listen():
    x1=x1x1['data']
    print x1x1
    print x1
  """


if __name__ == '__main__':
	  interact()
	
	
	
"""
in R

library(Rserve)
Rserve(args="--no-save") || Rserve() if not MacOS

"""

