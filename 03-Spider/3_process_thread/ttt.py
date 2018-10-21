
import datetime

bg = datetime.datetime.now()

n = 0
for i in range(5000000):
    n += 1

print(n)
end = datetime.datetime.now()
print('耗时：%s' % (end - bg))