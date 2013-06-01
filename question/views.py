from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse
from ibo2013.question.models import *
from ibo2013.question.forms import *
from django.db.models import Count
from django.db import connections

from django.contrib.auth.decorators import login_required

def view_exam(request,exam_id):
    try:
        exam_id = int(exam_id)
    except:
        raise Http404()
    
    try:
        exam = Exam.objects.get(id=exam_id)
    except:
        raise Http404()

    #return HttpResponse('<html><body>'+ str(exam.check_permission(request.user,Language.objects.get(id=1)))+'</body></html>')

    if request.method == 'POST':
        if "move" in request.POST:
            qid = int(request.POST["move"])
            q1 = ExamQuestion.objects.get(id=qid)
            if "up" in request.POST:
                try:
                    q2 = ExamQuestion.objects.get(exam=exam,position=q1.position-1)
                    q1.swap_position(q2)
                except ExamQuestion.DoesNotExist:
                    pass
            elif "down" in request.POST:
                try:
                    q2 = ExamQuestion.objects.get(exam=exam,position=q1.position+1)
                    q1.swap_position(q2)
                except ExamQuestion.DoesNotExist:
                    pass
            else:
                raise ValueError("move question must be either up or down")
        else:
    
            qf = AddQuestionForm(request.POST)
            if qf.is_valid():
                qfcd = qf.cleaned_data
                q = qf.save()
                eq = ExamQuestion(exam_id=exam.id,question_id=q.id,position=qfcd["position"],points=qfcd["points"])
                eq.save()
                exam.order_questions()
            else:
                raise ValueError("form is invalid")
    
    questions = ExamQuestion.objects.filter(exam=exam).order_by('position')
    qids = [q.id for q in questions]
    versionnodes = VersionNode.objects.filter(question__in=qids).values("language","question_id").annotate(max_version=Count('language'))
    form = AddQuestionForm()
     
    return render_to_response('exam_overview.html',{'exam':exam,'questions':questions,'versions':versionnodes,'form':form})


def translation_overview(request,exam_id,target_language_id):

    try:
        exam_id = int(exam_id)
        target_language_id = int(target_language_id)
        exam = Exam.objects.get(id=exam_id)
        language = Language.objects.get(id=target_language_id)
    except KeyError:
        raise Http404()

    questions = exam.examquestion_set.order_by('position')

    #selects all the most recent english versions of questions from this exam
    query = """SELECT * FROM (

        SELECT eq.*, vn.version, vn.id as vid
        FROM question_examquestion eq
        LEFT OUTER JOIN (
            SELECT *
            FROM question_versionnode
            WHERE language_id ='%s'
        ) AS vn ON eq.question_id = vn.question_id
        WHERE eq.exam_id='%s'
        ORDER BY position, version DESC
        ) AS t1
        GROUP BY position"""
    q1params = [1,exam_id] #todo: english = 1 is hardcoded as primary language

    primary_versions = ExamQuestion.objects.raw(query,q1params)

    #selects the most recent target translatsion versions of questions in exam
    query2 = """SELECT t1.*,tr.origin_id,tr.target_id FROM (
        SELECT eq.*, vn.version, vn.id as vid 
        FROM question_examquestion eq
        LEFT OUTER JOIN (
            SELECT *
            FROM question_versionnode
            WHERE language_id ='%s'
        ) AS vn ON eq.question_id = vn.question_id
        WHERE eq.exam_id='%s'
        ORDER BY position, version DESC
        )t1
        LEFT JOIN question_translation tr ON t1.vid = tr.target_id
        GROUP BY position"""
    q2params = [target_language_id,exam_id]

    target_versions = ExamQuestion.objects.raw(query2,q2params)

    pv = list(primary_versions)
    tv = list(target_versions)
    assert len(pv) == len(tv) #if not, you screwed up the queries

    questions = []
    for i in range(len(pv)):
        questions.append({"primary":pv[i],"target":tv[i]})
        if tv[i].vid is None:
            questions[i]["status"] = "not started"
        elif tv[i].origin_id != pv[i].vid:
            questions[i]["status"] = "needs update"
        else:
            questions[i]["status"] = "OK"
            
    return render_to_response('translation_overview.html',{'exam':exam,'questions':questions,'target_language_id':target_language_id})

def translate_question(request,question_id,target_language_id):
    try:
        question_id = int(question_id)
        target_language_id = int(target_language_id)
        question = Question.objects.get(id=question_id)
        language = Language.objects.get(id=target_language_id)
    except: 
        raise Http404()

    original = question.versionnode_set.filter(language=question.primary_language_id).order_by('-timestamp')[:1]

    versions = question.versionnode_set.filter(language=target_language_id).order_by('-timestamp')[:1]

    try:
        previous = versions[0].translation_target.all()[0].origin
        compare = previous.compare_with(original[0])
    except IndexError:
        compare = 'No previous translation found'

    if request.method == 'POST':
        form=EditQuestionForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            
            if not versions:
                vid = 1
            else:
                vid = versions[0].version+1

            v = VersionNode(
                question_id=question.id,
                language_id=target_language_id,
                version=vid,
                text=cd['text']
            )
            v.save()

            tr = Translation(
                language=v.language,
                origin=original[0],
                target=v
            )
            tr.save()
        
            return HttpResponse("done")

    if not versions:
        vtxt = ""
    else:
        vtxt = versions[0].text

    form=EditQuestionForm(initial={'text':vtxt})

    if not original:
        return HttpResponse("This question does not yet have a version in the primary language")

    return render_to_response('translate.html',{'original':original[0],'question':question,'compare':compare,'form':form})

@login_required
def view_question_history(request,question_id):
    
    try:
        question_id = int(question_id)
        question = Question.objects.get(id=question_id)
    except:
        raise Http404()

    versions = question.versionnode_set.all().order_by('-timestamp')
    return render_to_response('question_overview.html',{'question':question,'versions':versions})



def view_question(request,question_id):
    try:
        question_id = int(question_id)
        question = Question.objects.get(id=question_id)
    except:
        raise Http404()

    #todo: change this to include only the last version
    versions = question.versionnode_set.filter(language=question.primary_language).order_by('-timestamp')[:1]

    if request.method == 'POST':
        form = EditQuestionForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if len(versions) == 0:
                vnum = 1
                lang_id = question.primary_language_id
            else:
                vnum = versions[0].version + 1
                lang_id = versions[0].language_id            

            v = VersionNode(question_id=question.id,language_id=lang_id,version=vnum,text=cd['text'])
            v.save()
            versions = list(versions)
            versions.append(v)   
    
    form = EditQuestionForm()
    compare = ""
    if len(versions) == 2:
        compare = versions[0].compare_with(versions[1])

    return render_to_response('question_overview.html',{'question':question,'versions':versions,'form':form,'compare':compare})
        
