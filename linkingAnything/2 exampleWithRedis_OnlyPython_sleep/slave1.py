import redis
import time
r = redis.StrictRedis(host='localhost', port=6379, db=0)

# waiting for the master cleaning the database
x1=r.get("x1")
while x1 != None:
    x1=r.get("x1")
    time.sleep(0.001)

print "\n       slave1\n"

x1=100
r.set("x1",x1)


x2=r.get("x2")
while x2 == None:
    x2=r.get("x2")
    time.sleep(0.001)

print "\n             ", x2

#starting form slave1
x1+=1
r.set("x1",x1)

for i in range(10):
 xx2=x2
 while xx2 == x2:
     x2=r.get("x2")
     time.sleep(0.001)

 print "\n             ", x2

 x1+=1
 r.set("x1",x1)
