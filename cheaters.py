from ibo2013.question.models import *
from itertools import izip
import copy



def run():
    students = Student.objects.select_related().all().order_by('id')
    students2 = copy.copy(students) 
    exams = Exam.objects.filter(id__in=[4])

    for student in students:
        for exam in exams:
            answers = ExamAnswers.objects.filter(user=student.user,question__exam=exam).order_by('question__position') 
            #print answers.query
            if len(answers) == 0:
                print 'cont',student.user.first_name,student.user.last_name
                continue
            for student2 in students:
                if student2.id < student.id:
                    continue
                answers2 = ExamAnswers.objects.filter(user=student2.user,question__exam=exam).order_by('question__position') 

                ans1 = compact(serialize(answers))
                ans2 = compact(serialize(answers2))
                ham = hamming(ans1,ans2)
                print student,student2,ham
                es, created = ExamSimilarity.objects.get_or_create(user1=student.user,user2=student2.user,exam=exam)
                es.hamming = ham
                es.save()
                







def serialize(ea):
    ret = [None]*50*4
    for a in ea:
        for i in xrange(1,5):
            ret[(a.question.position-1)*4+i] = getattr(a,"answer{0}".format(i))

    return ret

def stringify(tf):
    if tf is None:
        return '2'
    elif tf == True:
        return '1'
    else:
        return '0'
    

def compact(ans):
    return "".join([stringify(x) for x in ans])

def hamming(str1,str2):
    assert len(str1) == len(str2)
    return sum(c1 != c2 for c1, c2 in izip(str1, str2)) 
