
import memcache


mc = memcache.Client(["127.0.0.1:10001"], debug=True)

mc.set("name", "python")

ret = mc.get("name")

print(ret)

print(mc.get())