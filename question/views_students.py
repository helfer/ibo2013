from django.shortcuts import render_to_response, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect
from ibo2013.question.models import *
from ibo2013.question.views_common import render_with_context
from django.contrib.auth.decorators import permission_required
from django.db.models import Count
from django.db import connections
from django.template import RequestContext
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from ibo2013.question import qml
from django.db.models import Q
from xml.etree import ElementTree as et

@login_required
@permission_required('question.is_jury')
def question(request,language_id,exam_id,question_position):

    #if (not request.user.groups) and (int(exam_id) not in [1,2]):
    #    raise PermissionDenied() #TODO: just a hack to keep people out
    try:
        question_position = int(question_position)
        exam_id = int(exam_id)
        language = Language.objects.get(id=language_id)
        question = Question.objects.get(exam__id=exam_id,examquestion__position=question_position)
        eq = ExamQuestion.objects.get(question=question,exam=exam_id)
        num_questions = ExamQuestion.objects.filter(exam=exam_id).count()
    except:
        raise Http404()
    flag = ExamFlags.objects.filter(user=request.user,question=eq).count() > 0
    
    try:
        a = ExamAnswers.objects.get(user=request.user,question=eq)
        this_answer = [(3,a.answer1),(4,a.answer2),(5,a.answer3),(6,a.answer4)] 
    except:
        this_answer = [(3,None),(4,None),(5,None),(6,None)]
    
    try:
        vnode = question.versionnode_set.filter(language=language.id).order_by('-timestamp')[0]
        xmlq = qml.QMLquestion(vnode.text)
        struct = xmlq.get_texts_nested(prep=True)
    except: 
        return render_with_context(request,'students_questionview.html',
        {'available':False,
        'exam_id':exam_id,
        'lang_id':language_id,
        'pos':question_position,
        'language':language,
        'question':question,
        'user':request.user,
        'eq':eq,
        'flag':flag,
        'answers':this_answer,
        'num_questions':num_questions
    })


    return render_with_context(request,'students_questionview.html',
        {'available':True,
        'exam_id':exam_id,
        'lang_id':language_id,
        'pos':question_position,
        'language':language,
        'question':question,
        'vnode':vnode,
        'struct':struct,
        'user':request.user,
        'eq':eq,
        'flag':flag,
        'answers':this_answer,
        'num_questions':num_questions
    })


@login_required
@permission_required('question.is_jury')
def examview(request,language_id,exam_id):
    
    #if (not request.user.is_staff) and (int(exam_id) not in [1,2]):
    #    raise PermissionDenied() #TODO: just a hack to keep people out

    try:
        exam = Exam.objects.get(id=exam_id)
        language = Language.objects.get(id=language_id)
    except:
        raise Http404()

    answers = ExamAnswers.objects.filter(user=request.user)
    flags = ExamFlags.objects.filter(user=request.user)
    questions = ExamQuestion.objects.filter(exam=exam).order_by('category','position')
    categories = CategoryTranslation.objects.filter(language=1).order_by('category')
    categories = dictify(categories,'category_id')

    cid = -1
    objs = []
    for q in questions:
        if q.category_id != cid:
            cid = q.category_id
            objs.append({'cat':categories[cid],'questions':[]})

        flag = False
        for f in flags:
            if f.question_id == q.id:
                flag= True
                break
        status = 'empt'
        for a in answers:
            if a.question_id == q.id:
                arr = [a.answer1 is not None,a.answer2 is not None,a.answer3 is not None,a.answer4 is not None]
                if any(arr):
                    status = "need"
                if all(arr):
                    status = "done"
        if flag:
            status += " flag" 

        cq = {'q':q,'status':status,'flag':flag }
        objs[-1]['questions'].append(cq)

        


    return render_with_context(request,'students_examview.html',{
        'lang_id':language_id,
        'exam_id':exam_id,
        'categories':objs,
        'user':request.user
        })



def dictify(obj_list,key):
    ret = {}
    for obj in obj_list:
        ret[getattr(obj,key)] = obj
    return ret
