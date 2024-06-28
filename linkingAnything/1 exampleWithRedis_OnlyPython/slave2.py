import redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)

# waiting for the master cleaning the database
x2=r.get("x2")
while x2 != None:
    x2=r.get("x2")

print "\n       slave2\n"

x2=200
r.set("x2",x2)


x1=r.get("x1")
while x1 == None:
    x1=r.get("x1")

print "\n             ", x1


for i in range(10):
 xx1=x1
 while xx1 == x1:
     x1=r.get("x1")

 print "\n             ", x1

 x2+=1
 r.set("x2",x2)
