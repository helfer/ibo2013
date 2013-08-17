from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import Http404, HttpResponse, HttpResponseRedirect
from ibo2013.question.models import *
from ibo2013.question.forms import *
from ibo2013.question.views_common import render_with_context
import ibo2013.question #circular import fix?
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
import itertools

@login_required
#@permission_required('question.is_jury')
def question(request,language_id,exam_id,question_position):
    try:
        question_position = int(question_position)
        exam_id = int(exam_id)
        exam = Exam.objects.get(id=exam_id,staff_only=0)
        language = Language.objects.get(id=language_id)
        question = Question.objects.get(exam__id=exam_id,examquestion__position=question_position)
        eq = ExamQuestion.objects.get(question=question,exam=exam_id)
        num_questions = ExamQuestion.objects.filter(exam=exam_id).count()
    except:
        raise Http404()
    flag = ExamFlags.objects.filter(user=request.user,question=eq).count() > 0
    
    if exam.start == False: #or exam.stop == True:
        return redirect('/students/{0}/overview/{1}/'.format(language_id,exam_id))

    data = False
    index = 10
    elog = ExamAjaxLog(user=request.user,question=eq,index=index,data=data,response=str(language.id))

    try:
        a = ExamAnswers.objects.get(user=request.user,question=eq)
        this_answer = [(3,a.answer1),(4,a.answer2),(5,a.answer3),(6,a.answer4)] 
    except:
        elog.response = elog.response + ' first'
        this_answer = [(3,None),(4,None),(5,None),(6,None)]
    
    try:
        vnode = question.versionnode_set.filter(language=language.id).order_by('-version')[0]
        xmlq = qml.QMLquestion(vnode.text)
        struct = xmlq.get_texts_nested(prep=True)
    except: 
        elog.response = elog.response + ' unavailable'
        elog.save()
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

    langs = Language.objects.filter(id__in=[1,2])
    picker = PickLanguageForm(request.user,language_id,request,languages = langs,initial={'language':request.path})        

    if not request.user.username.startswith("test"):
        delegation = request.user.delegation_set.all()[0]
        picker = PickLanguageForm(request.user,language_id,request,languages=delegation.exam_languages.all(),initial={'language':request.path})        
        #picker = PickLanguageForm(request.user,language_id,request,initial={'language':request.path})        
    elog.response = elog.response + " OK"
    elog.save()
    return render_to_response('students_questionview.html',
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
        'num_questions':num_questions,
        'lang_picker':picker
    })


@login_required
def resultview(request):
    return render_to_response('students_results_overview.html',{'user':request.user})
    #make a view similar to jury, use results_base
 
#may throw exception if user_id is not valid
def theoryresults_meta(request,user_id=None):
 
    exams = Exam.objects.filter(staff_only=False)
    ae = []
    if user_id is None:
        selected_user = request.user
    else:
        selected_user = User.objects.get(id=user_id)

    #print 'userid',user_id,'sel',selected_user.id

    for exam in exams:
        ex = {'exam':exam}
        answers = list(ExamAnswers.objects.filter(user=selected_user,question__exam=exam).order_by('question__position'))
        solution = ExamAnswers.objects.filter(user=303,question__exam=exam).order_by('question__position') 
        lines = [] 
        i = 0
        total = 0
        for sol in solution:
            if i >= len(answers) or sol.question_id != answers[i].question_id:
                ans = ExamAnswers(user=selected_user,question=sol.question)
            else:
                ans = answers[i]
                i += 1

            sc = score(ans,sol)
            lines.append(sc)
            total += sc['score']
        ex['list'] = lines
        ex['total'] = total
        ae.append(ex)

    try:
        lang_id =  selected_user.delegation_set.all()[0].exam_languages.all()[0].id
    except:
        lang_id = 1

    return (ae,lang_id)

@login_required
def theoryresults(request,user_id=None):
    ae,lang_id = theoryresults_meta(request,user_id)
    return render_to_response('students_results_theory.html',{'ae':ae,'lang_id':lang_id})
    #list TTFT, solution, score, link to questionview in iframe

# score answers and return pattern TTFT
def score(ans,sol):
    grading = {0:0,1:0,2:0.2,3:0.6,4:1}
    ret = {'ans':ans.prettystring(),'sol':sol.prettystring()}
    correct = sum(itertools.imap(str.__eq__, ret['ans'], ret['sol']))
    ret['score'] = grading[correct]
    return ret

@login_required
def practicalresults(request):
    context = ibo2013.question.views_jury.results_meta(request)
    return render_to_response('students_results_practical.html',context)
    #use same view as jury, but list only this student's results


@login_required
#@permission_required('question.is_jury')
def examview(request,language_id,exam_id):
#    if int(exam_id)!=4:
#        exam_id=4
    if request.user.groups.all().count() == 0:
        exam_id = 2
 
    #if (not request.user.is_staff) and (int(exam_id) not in [1,2]):
    #    raise PermissionDenied() #TODO: just a hack to keep people out

    try:
        exam = Exam.objects.get(id=exam_id,staff_only=0)
        language = Language.objects.get(id=language_id)
    except:
        raise Http404()

    answers = ExamAnswers.objects.filter(user=request.user)
    flags = ExamFlags.objects.filter(user=request.user)
    questions = ExamQuestion.objects.filter(exam=exam).order_by('category','position')
    categories = CategoryTranslation.objects.filter(language=language_id).order_by('category')
    categories = dictify(categories,'category_id')
    cats_en = CategoryTranslation.objects.filter(language=1).order_by('category')
    cats_en = dictify(cats_en,'category_id')
    
    data = False
    index = 11
    elog = ExamAjaxLog(user=request.user,question_id=36,index=index,data=data,response=str(language.id))
    elog.save()

    cid = -1
    objs = []
    for q in questions:
        if q.category_id != cid:
            cid = q.category_id
            try:
                objs.append({'cat':categories[cid],'questions':[]})
            except:
                objs.append({'cat':cats_en[cid],'questions':[]})

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

    langs = Language.objects.filter(id__in=[1,2])
    picker = PickLanguageForm(request.user,language_id,request,languages = langs,initial={'language':request.path})        
    
    if not request.user.username.startswith("test"):
        delegation = request.user.delegation_set.all()[0]
        picker = PickLanguageForm(request.user,language_id,request,languages=delegation.exam_languages.all(),initial={'language':request.path})        

    return render_to_response('students_examview.html',{
        'lang_id':language_id,
        'exam_id':exam_id,
        'categories':objs,
        'user':request.user,
        'lang_picker':picker})


"""redirect based on chosen language for this student"""
@login_required
def theory(request):
    
    try:
        delegation = request.user.delegation_set.all()[0]
    except:
        return HttpResponse("We don't know what delegation you are with. Please notify exam staff immediately",content_type="text/plain")

    try:
        lang = delegation.exam_languages.all().order_by('-id')[0]
    except:
        lang = Language.objects.get(id=1)

    return redirect("/students/{0}/overview/3/".format(lang.id))





def dictify(obj_list,key):
    ret = {}
    for obj in obj_list:
        ret[getattr(obj,key)] = obj
    return ret
