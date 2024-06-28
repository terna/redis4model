import pyRserve


 
def main():

  cn=pyRserve.connect(host="localhost")
  cn.r('library(rredis)')
  cn.r('redisConnect()')

  x=42
  num=cn.r('redisPublish("ch1",'+str(x)+')')

  print "Published on channel ch1 with "+str(num)+" listener/s"

  
 
if __name__ == '__main__':
  main()


"""
in R

library(Rserve)
Rserve(args="--no-save") || Rserve() if not MacOS

"""
