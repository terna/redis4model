import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

chn='ch1'

#num=r.publish(chn, 42)
#print num


sub=r.pubsub()
sub.subscribe(chn)
print sub.listen().next()
num=r.publish(chn, 420)
print num
print sub.listen().next()
