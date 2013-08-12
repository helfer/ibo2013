from ibo2013.question.models import *
import math
from django.db.models import Q

fs = FinalScore.objects.filter(~Q(id=141))



sums = [0]*4
zerocount = 0

count = 0.0
for f in fs:
    if f.auth_user_id in [141,39,303,132]:
	print "delete",f.auth_user_id
	f.delete()
	
fs = FinalScore.objects.all()
for f in fs:
    count += 1
    for i in range(1,5):
        score = getattr(f,"p{0}".format(i))
	assert score != 0
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
        sds[i-1] += (avgs[i-1] - score)**2
print 'count',count
print 'before divide',sds
sds = map(lambda x:x/(count-1),sds)
print 'sds after divide',sds
sds = map(math.sqrt,sds)
print 'sds final',sds

zums = [0]*4
var = [0]*4
for f in fs:
    for i in range(1,5):
        score = float(getattr(f,"p{0}".format(i)))
        tscore = (score-avgs[i-1])/sds[i-1]
        zums[i-1] += tscore
        setattr(f,"t{0}".format(i),tscore)
        
    #f.save()

vrs = [0]*4
for f in fs:
    for i in range(1,5):
        tscore = float(getattr(f,"t{0}".format(i)))
        vrs[i-1] += (tscore**2)/count
    print f.id
    f.save()
print "sums",zums
print "var",vrs	
print "done"

        
