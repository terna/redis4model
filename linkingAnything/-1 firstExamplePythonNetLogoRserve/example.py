import pyRserve

cn=pyRserve.connect(host="localhost")

a=cn.r.a

print a

cn.close()

print "connection closed"
