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
            print "z",f.auth_user_id
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

zums = [0]*4
var = [0]*4
for f in fs:
    for i in range(1,5):
        score = float(getattr(f,"p{0}".format(i)))
        if score == 0:
            continue
        tscore = (score-avgs[i-1])/sds[i-1]
        zums[i-1] += tscore
        setattr(f,"t{0}".format(i),tscore)
        
    #f.save()


print "sums",zums
print "done"

        
