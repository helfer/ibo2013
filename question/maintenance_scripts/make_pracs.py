from ibo2013.question.models import *


def make_practical_questions(lst):
    prac = PracticalExam.objects.all().order_by("position")
    assert len(lst) == prac.count()

    i = 0
    for p in prac:
        for j in xrange(1,lst[i]+1):
            pq = PracticalQuestion(practical=p,position=j)
            print pq
            pq.save()
        i +=1

    print "done"
    return
