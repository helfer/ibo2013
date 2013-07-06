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
from django.db.models import Q

@login_required
@staff_member_required
def view_exam(request,exam_id):
    try:
        exam_id = int(exam_id)
        exam = Exam.objects.get(id=exam_id)
    except:
        raise Http404()
    
    if request.method == 'POST':
        print request.POST
        if "up" in request.POST or "down" in request.POST or "delete" in request.POST:
            qid = int(request.POST["qid"])
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
            elif "delete" in request.POST:
                q1.delete()
            else:
                raise ValueError("move question must be either up or down")
        elif "update" in request.POST:
            try:
                q = ExamQuestion.objects.get(id=long(request.POST["qid"]))
                form = UpdateCategoryForm(request.POST,instance=q)
                if form.is_valid():
                    form.save()
            except:
                raise ValueError("your points update does not compute")
        elif "addquestion" in request.POST:
    
            qf = AddQuestionForm(request.POST)
            if qf.is_valid():
                qfcd = qf.cleaned_data
                q = qf.save(commit=False)
                q.primary_language_id = 1 #English, hardcoded
                q.save()
                eq = ExamQuestion(exam_id=exam.id,question_id=q.id,position=qfcd["position"],points=qfcd["points"],category=qfcd['category'])
                eq.save()
                xmlq = qml.QMLquestion.from_template(q.id)
                xmlq.assign_initial_id(q.id)
                vtext = xmlq.zackzack() 
                vn = VersionNode(question=q,language_id=q.primary_language_id,version=1,text=vtext,comment='auto generated stub')
                vn.save()
                exam.order_questions()
                return redirect(view_question,q.id)
            else:
                raise ValueError("form is invalid")
    
        elif "insertquestion" in request.POST:
            form = AddExamquestionForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                eq = ExamQuestion(exam=exam,question=cd['question'],position=cd['position'],points=1,category_id=1)
                eq.save()
                exam.order_questions()
        else:
            raise KeyError("unkown form submitted")

    questions = ExamQuestion.objects.filter(exam=exam).order_by('position')
    qids = [q.id for q in questions]
    #versionnodes = VersionNode.objects.filter(question__in=qids).values("language","question_id").annotate(max_version=Count('language'))
    form = AddQuestionForm()
    insertform = AddExamquestionForm()#this adds existing examquestions
    objs = []
    for q in questions:
       objs.append({
        'form': UpdateCategoryForm(instance=q),
        'q':q})

    return render_to_response('staff_examview.html',
        {'exam':exam,
        'questions':objs,
        #'catform':catform,
        #'versions':versionnodes,
        'form':form,
        'insertform':insertform
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
        if len(versions) == 0:
            vnum = 1
            lang_id = question.primary_language_id
        else:
            vnum = versions[0].version + 1
            lang_id = versions[0].language_id            
            
        if "reident" in request.POST:
            print "newform"
            xmlq = qml.QMLquestion(versions[0].text)
            xmlq.reassign_identifiers(question.id) 
            v = VersionNode(question_id=question.id,language_id=lang_id,version=vnum,text=xmlq.zackzack())
            v.save()
            return redirect(request.path) #POST,GET redirect for instant reload   

        else:
            if mode == "normal":
                print "newform"
                xmlq = qml.QMLquestion(versions[0].text)
                form = QMLform(request.POST,qml=xmlq)
                if form.is_valid():
                    print "isvalid"
                    print form.cleaned_data
                    xmlq.update(form.cleaned_data)
                   
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

                    xmlq = qml.QMLquestion(cd['text'])
                    xmlq.assign_initial_id(question.id)
                    v = VersionNode(question_id=question.id,language_id=lang_id,version=vnum,text=xmlq.zackzack())
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
        
@staff_member_required
def view_categories(request):

    categories = QuestionCategory.objects.all().order_by('position')
    errors = ""
    addform = AddCategoryForm()
    if request.method == "POST":
        if "submit" in request.POST:
            addform = AddCategoryForm(request.POST)
            if addform.is_valid():
                cd = addform.cleaned_data
                cat = QuestionCategory(name=cd['name'],position=cd['position'])
                cat.save()
                trans = CategoryTranslation(language_id=1,text=cd['title'])
                cat.categorytranslation_set.add(trans)
                cat.save()
                return redirect("/staff/categories?success")
            else:
                print "form contains errors"
        if "update" in request.POST:
            try:
                #insecure, but only staff have access
                print "cat_id " + request.POST["cat_id"]
                instance=QuestionCategory.objects.get(id=int(request.POST['cat_id']))
                f = EditCategoryForm(request.POST,instance=instance)
                if f.is_valid():
                    f.save()
                    return redirect("/staff/categories?success")
                else:
                    errors = form.errors
            except:
                print "this category doesn't exist"
    else:
        pass
    cats = []
    for c in categories:
        cats.append({'form':EditCategoryForm(instance=c),'cat':c})


    return render_to_response('staff_categories.html', {'categories':cats,'errors':errors,'addform':addform})

@staff_member_required
def translate_categories(request,lang_id):

    try:
        lid = int(lang_id)
        language = Language.objects.get(pk=lid)
        english = Language.objects.get(pk=1)
    except:
        raise Http404()


    if request.method == 'POST':
        try:
            inst = CategoryTranslation.objects.get(category=int(request.POST['cat_id']),language=lid)
        except:
            inst = CategoryTranslation(category_id=int(request.POST['cat_id']),language_id=lid)
            inst.save()
        frm = TranslateCategoryForm(request.POST,instance=inst)
        if frm.is_valid():
            frm.save()


    cats = QuestionCategory.objects.all().order_by('position')

    objs = []
    for c in cats:
        trans = c.categorytranslation_set.filter(Q(language=language) | Q(language=english)).order_by('language')
        print "len" + str(len(trans))
        orig = trans[0]
        if len(trans) == 1:
            frm = TranslateCategoryForm()
        else:
            frm = TranslateCategoryForm(instance=trans[1])
            
        objs.append({"orig":orig,"form":frm})


    print objs

    return render_to_response('staff_categories_trans.html',{'objs':objs})




