from django.shortcuts import render_to_response, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect
from ibo2013.question.models import *
from ibo2013.question.forms import *
from django.db.models import Count
from django.db import connections
from django.template import RequestContext
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from ibo2013.question import qml


@login_required
@staff_member_required
def view_exam(request,exam_id):
    try:
        exam_id = int(exam_id)
        exam = Exam.objects.get(id=exam_id)
    except:
        raise Http404()

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
        elif "update" in request.POST:
            try:
                q = ExamQuestion.objects.get(id=long(request.POST["qid"]))
                q.points = float(request.POST["points"])
                q.save()
            except:
                raise ValueError("your points update does not compute")
        else:
    
            qf = AddQuestionForm(request.POST)
            if qf.is_valid():
                qfcd = qf.cleaned_data
                q = qf.save(commit=False)
                q.primary_language_id = 1 #English, hardcoded
                q.save()
                eq = ExamQuestion(exam_id=exam.id,question_id=q.id,position=qfcd["position"],points=qfcd["points"])
                eq.save()
                vtext = qml.QMLquestion.from_template(q.id).zackzack()
                vn = VersionNode(question=q,language_id=q.primary_language_id,version=1,text=vtext,comment='auto generated stub')
                vn.save()
                exam.order_questions()
                return redirect(view_question,q.id)
            else:
                raise ValueError("form is invalid")
    
    questions = ExamQuestion.objects.filter(exam=exam).order_by('position')
    qids = [q.id for q in questions]
    #versionnodes = VersionNode.objects.filter(question__in=qids).values("language","question_id").annotate(max_version=Count('language'))
    form = AddQuestionForm()

    return render_to_response('staff_examview.html',
        {'exam':exam,
        'questions':questions,
        #'versions':versionnodes,
        'form':form
        })

@login_required
@staff_member_required
def view_question_history(request,question_id):
    
    try:
        question_id = int(question_id)
        question = Question.objects.get(id=question_id)
    except:
        raise Http404()

    versions = question.versionnode_set.all().order_by('-timestamp')
    return render_to_response('question_overview.html',{'question':question,'versions':versions})




@login_required
@staff_member_required
def view_question(request,qid=None,mode="normal"):
    try:
        question_id = int(qid)
        question = Question.objects.get(id=question_id)
    except:
        raise Http404()

    #todo: change this to include only the last version
    versions = question.versionnode_set.filter(language=question.primary_language).order_by('-timestamp')[:1]

    if request.method == 'POST':
        print request.POST
        if mode == "normal":
            print "newform"
            xmlq = qml.QMLquestion(versions[0].text)
            form = QMLform(request.POST,qml=xmlq)
            if form.is_valid():
                print "isvalid"
                print form.cleaned_data
                xmlq.update(form.cleaned_data)
                if len(versions) == 0:
                    vnum = 1
                    lang_id = question.primary_language_id
                else:
                    vnum = versions[0].version + 1
                    lang_id = versions[0].language_id            
                
                v = VersionNode(question_id=question.id,language_id=lang_id,version=vnum,text=xmlq.zackzack())
                v.save()
                versions = list(versions)
                versions.append(v)   
                
                return redirect(request.path) #POST,GET redirect for instant reload   
            else:
                print "haserrors"
                print form.errors

        elif mode == "xml": #XXX: legacy compatibility, to be removed
            print "legacy"
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
                
                return redirect(request.path) #POST,GET redirect for instant reload   
        else:
            raise ValueError("no such view mode: >" + str(mode)+"<")
    #print versions[0].text   
    
    #request method is not POST, no form was submitted
    else:
        if len(versions) > 0 and mode == "normal":
            print "xmlquestion"
            try:
                xmlq = qml.QMLquestion(versions[0].text)
                print xmlq.summary()
                form = QMLform(qml=xmlq)
            except Exception as e:
                print "exception"
            #    if versions[0].text.startswith('<question'):
            #        #this should probably be xml, raise exception
            #        raise e
            #    else:
                print "redirect"
                return redirect("/staff/question/"+str(question_id)+"/xml/")
            
        else:
            init = {}
            if len(versions) > 0:
                init = {
                    'text':versions[0].text,
                    'comment':versions[0].comment,
               }

            form = EditQuestionForm(initial=init)
    
    compare = ""
    #if len(versions) == 2:
    #    compare = versions[0].compare_with(versions[1])

    return render_to_response('staff_questionview.html',
        {'question':question,
        'versions':versions,
        'form':form,
        'compare':compare,
        'viewmode':mode})
        

