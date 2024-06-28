import redis
import threading
import time
 
def callback():
  r = redis.client.StrictRedis()
  sub = r.pubsub()
  sub.subscribe('clock')
  while True:
    for m in sub.listen():
      print m #'Recieved: {0}'.format(m['data'])

if __name__ == '__main__':
	  callback()
