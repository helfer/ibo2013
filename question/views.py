from django.shortcuts import render_to_response
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

def render_with_context(request,*args,**kwargs):
    lang_id = args[1]["lang_id"]
    picker = PickLanguageForm(request.user,lang_id,request,initial={'language':request.path})
    kwargs['context_instance'] = RequestContext(request)
    args[1]["lang_picker"] = picker
    return render_to_response(*args,**kwargs)


#decorator that checks which permissions a user has.
def permission_check(f):
    def secure_f(*args,**kwargs):
        request = args[0]
        lang_id = kwargs['lang_id']
        permissions = ['read']

        if request.user.is_superuser:
            permissions = ['read','write','admin']
        else:

            if  Language.objects.get(id=lang_id).editors.filter(id=request.user.id).exists():
                permissions.append('write')
            if  Language.objects.get(id=lang_id).coordinators.filter(id=request.user.id).exists():
                permissions.append('admin')

        print args[0].user,kwargs,permissions

        res = f(*args,permissions=permissions,**kwargs)

        return res

    return secure_f
        
    
@login_required
@permission_check
def jury_overview(request,lang_id=1,permissions=None):
    try:
        lang_id = int(lang_id)
    except:
        raise Http404()

    exams = Exam.objects.all()

    for e in exams:
        e.load_question_status(lang_id)
       
    picker = PickLanguageForm(request.user,lang_id,request,initial={'language':request.path})
    print picker   
    print permissions 

    return render_with_context(request,'jury_overview.html',{'exams':exams,'lang_id':lang_id,'perms':permissions})

@login_required
@permission_check
def jury_profile(request,lang_id=1,permissions=None):

    try:
        lang_id = int(lang_id)
        language = Language.objects.get(id=lang_id)
    except:
        raise Http404()

    add_form = AddLanguageForm()
    edit_form = EditLanguageForm(instance=language)

    if request.method == "POST":
        if "editlanguage" in request.POST and 'admin' in permissions:
            print "in edit"
            form = EditLanguageForm(request.POST,instance=language)
            if form.is_valid():
                print form
                lang = form.save()
                print "changes saved"
                #don't want people to remove their own permissions
                if request.user.id not in form.cleaned_data['coordinators']:
                    lang.coordinators.add(request.user)
            edit_form = form
        elif "addlanguage" in request.POST:
            print "in add"
            form = AddLanguageForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                lang = Language(name=cd['name'])
                lang.save()
                lang.editors.add(request.user)
                lang.coordinators.add(request.user)
                for exam in Exam.objects.all():
                    exam.languages.add(lang)
                #switch view to new language
                return HttpResponseRedirect('/jury/'+str(lang.id)+'/')
            else:
                add_form = form
        else:
            print "unknown form"
            


    exams = Exam.objects.all()
    languages = Language.objects.get(id=1).coordinators.all()
    languages = request.user.coordinator_set.all() | request.user.editor_set.all()
    return render_with_context(request,'jury_profile.html',{'exams':exams,'perms':permissions,'languages':languages,'addform':add_form,'editform':edit_form,'lang_id':language.id,'language':language})

#@login_required
#def jury_manage_permissions(request,exam_id,lang_id=1):
#    #TODO make sure user has coordinator privilege on exam/lang combination
#    users = {}
#    return render_to_response('jury_manage_permissions.html',{'lang_id':lang_id,'exam_id':exam_id,'users':users})


@login_required
@permission_check
def jury_examview(request,exam_id=1,lang_id=1,permissions=None):
    try:
        lang_id = int(lang_id)
        exam_id = int(exam_id)
        exam = Exam.objects.get(id=exam_id)
    except:
        raise Http404()

    exams = Exam.objects.all()

    exam.load_question_status(lang_id)
    questions = exam.question_status

    return render_with_context(request,'jury_examview.html',{'exam':exam,'exams':exams,'lang_id':lang_id,'questions':questions})

@login_required
@staff_member_required
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


@login_required
@permission_check
def translation_overview(request,exam_id,lang_id=1,permissions=None):

    raise Exception("deprecated function")

    try:
        exam_id = int(exam_id)
        target_language_id = int(lang_id)
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

@login_required
@permission_check
def jury_questionview(request,exam_id=1,question_position=1,lang_id=1,permissions=None):
    try:
        question_position = int(question_position)
        target_language_id = int(lang_id)
        exam_id = int(exam_id)
        exam = Exam.objects.get(id=exam_id)
        language = Language.objects.get(id=target_language_id)
    except: 
        raise Http404()

    question = Question.objects.get(exam__id=exam_id,examquestion__position=question_position)
    exams = Exam.objects.all()

    original = question.versionnode_set.filter(language=question.primary_language_id).order_by('-timestamp')[:1]

    versions = question.versionnode_set.filter(language=target_language_id).order_by('-timestamp')[:1]


    if request.method == 'POST':
        form=EditQuestionForm(request.POST)
        print form.is_bound,request.POST
        if not ('write' in permissions or 'admin' in permissions):
            raise PermissionDenied()
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
                text=cd['text'],
                flag=cd['flag'],
                checkout=cd['checkout'],
                comment=cd['comment']
            )
            v.save()

            tr = Translation(
                language=v.language,
                origin=original[0],
                target=v
            )
            tr.save()
       
            #return HttpResponse("done") 
            versions = question.versionnode_set.filter(language=target_language_id).order_by('-timestamp')[:1]
        else: 
            print "form contains errors"
            print form.errors, form.is_valid(),form.is_bound
            print "those were the errors"
    try:
        previous = versions[0].translation_target.all()[0].origin
        compare = previous.compare_with(original[0])
    except IndexError:
        compare = original[0].text

    if not versions:
        initial = {}
    else:
        initial = {'text':versions[0].text,'flag':versions[0].flag,'checkout':versions[0].checkout,'comment':versions[0].comment}

    if 'write' in permissions or 'admin' in permissions:
        form=EditQuestionForm(initial=initial)
    else:
        form=ViewQuestionForm(initial=initial)

    exam.load_question_status(target_language_id)
    
    if not original:
        return HttpResponse("This question does not yet have a version in the primary language")

    return render_with_context(request,'jury_questionview.html',{'exam':exam,'lang_id':target_language_id,'pos':question_position,'status':exam.question_status,'exams':exams,'original':original[0],'question':question,'compare':compare,'form':form,'perms':permissions})

@login_required
def view_question_history(request,question_id):
    
    try:
        question_id = int(question_id)
        question = Question.objects.get(id=question_id)
    except:
        raise Http404()

    versions = question.versionnode_set.all().order_by('-timestamp')
    return render_to_response('question_overview.html',{'question':question,'versions':versions})




@login_required
def view_question(request,question_id):
    try:
        question_id = int(question_id)
        question = Question.objects.get(id=question_id)
    except:
        raise Http404()

    #todo: change this to include only the last version
    versions = question.versionnode_set.filter(language=question.primary_language).order_by('-timestamp')[:1]

    if request.method == 'POST':
        if versions[0].text.startswith("<question"):
            print "newform"
            xmlq = qml.QMLquestion(versions[0].text)
            form = QMLform(request.POST,qml=xmlq)
            if form.is_valid():
                xmlq.update(form.cleaned_data)
                print "zackzack",xmlq.zackzack(),"schwupp"
            else:
                print form.errors

        else: #XXX: legacy compatibility, to be removed
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

    print versions[0].text   
 
    if versions[0].text.startswith("<question"):
        print "xmlquestion"
        xmlq = qml.QMLquestion(versions[0].text)
        print xmlq.summary()
        form = QMLform(qml=xmlq)
    else:
        form = EditQuestionForm()
    compare = ""
    if len(versions) == 2:
        compare = versions[0].compare_with(versions[1])

    return render_to_response('question_overview.html',{'question':question,'versions':versions,'form':form,'compare':compare})
        

