from ibo2013.question.models import *
import math
from django.db.models import Q

fs = FinalScore.objects.filter(~Q(id=141))



sums = [0]*4
zerocount = 0

count = 0
for f in fs:
    count += 1
    for i in range(1,5):
        score = getattr(f,"p{0}".format(i))
        if score == 0:
            count -= 1
            zerocount += 1
            continue
        sums[i-1] += float(score)

print 'zero',zerocount
print 'count',count
print 'sums',sums
avgs = map(lambda x:x/count,sums)
print 'avgs',avgs

sds = [0]*4
for f in fs:
    for i in range(1,5):
        score = float(getattr(f,"p{0}".format(i)))
        if score == 0:
            continue
        sds[i-1] += (avgs[i-1] - score)**2
print 'count',count
print 'before divide',sds
sds = map(lambda x:x/count,sds)
print 'sds after divide',sds
sds = map(math.sqrt,sds)
print 'sds final',sds
