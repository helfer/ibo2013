import json
import numpy as np
from ibo2013.question.models import *
from django.contrib.auth.models import User
import datetime



def make_student_json():
    students = Student.objects.filter(testbit=False).select_related()
    sid = linear_projection(students,k='user_id')
    #print "studentlen ", len(list(students))
    ret = []
    for s in students:
        details = {
            'id':sid[s.user.id],
            'real_id':s.user.id,
            'fname':s.user.first_name,
            'lname':s.user.last_name,
            'code':s.individual_id,
            'delegation':s.delegation.name
        }
        ret.append(details)
    print json.dumps(ret)


def make_question_json():
    questions = ExamQuestion.objects.filter(exam=3).select_related().order_by('question__examquestion__position')
    qid = linear_projection(questions)
    ret = []
    for q in questions:
        details = {
            'id':qid[q.id],
            'real_id':q.id,
            'category':q.category.name
        }
        ret.append(details)
    print json.dumps(ret)

def run(start=0,end=1000000,examid=3):
  pass
  students = Student.objects.filter(testbit=False).select_related()
  print "studentlen ", len(list(students))
  questions = ExamQuestion.objects.filter(exam=examid).order_by('question__examquestion__position')
  log = ExamAjaxLog.objects.filter(question__exam=examid).select_related().order_by('timestamp')[start:end]
  sid = linear_projection(students,k='user_id')
  qid = linear_projection(questions)

  scores = np.zeros((len(sid),len(qid),4))#three dim, for each question 4 answers
  focus = {}

  events = []

  for item in log:
    try:
        si = sid[item.user.id]
    except:
        print "user id {0} not in student list".format(item.user.id)
        continue
    qi = qid.get(item.question.id,-1)
    e = {
      'tstamp':item.timestamp.isoformat(),
      'sid':si,
      'qid':qi,
      'prev_qid':None, #used to indicate where focus came from
      'score':None,
      'prev_score':None, #used to indicate previous score
      'focus':None,
      'flag':None
        }
    if item.index == 0:
      #flag
      e['flag'] = item.data 
    elif item.index <= 4:
      #update score
      #TODO: give the actual score, not the number of true!
      try:
        sc = scores[si,qi]
        e['prev_score'] = np.sum(sc)
        if(item.data):
          sc[item.index-1] = 1
        else:
          sc[item.index-1] = 0
        e['score'] = np.sum(sc)
      except:
        print item.index, sc
    elif item.index == 10:
      #set focus
      e['focus'] = True
      e['prev_qid'] = focus.get(si,-1)
      focus[si] = qi
    elif item.index == 11:
      #take focus away
      e['qid'] = focus.get(si,-1) #beacause otherwise it's always 36
      focus[si] = -1
      e['focus'] = False
    else:
      raise Exception("unknown index: " + item.index)
    if(e['qid'] >= 0):
      events.append(e)
    else:
      pass
      #print "skipping",e
  with open("examlog.json","w") as f:
    f.write(json.dumps(events))

  return True

#returns a projection from id to 1..4
def linear_projection(qset,k='id'):
  ret = {}
  for i,item in enumerate(qset):
    ret[getattr(item,k)] = i

  return ret
