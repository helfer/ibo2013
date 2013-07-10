from django.shortcuts import render_to_response,redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect
from ibo2013.question.models import *
from ibo2013.question.forms import *
from django.db.models import Count
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from ibo2013.question.qml import *
from ibo2013.question.views_common import *        
from ibo2013.question import utils   
 
@login_required
@permission_check
def overview(request,lang_id=1,permissions=None):
    try:
        lang_id = int(lang_id)
    except:
        raise Http404()

    if request.user.is_staff:
        exams = Exam.objects.all()
    else:
        exams = Exam.objects.filter(staff_only=False)

    for e in exams:
        e.load_question_status(lang_id)
       
    #picker = PickLanguageForm(request.user,lang_id,request,initial={'language':request.path})

    return render_with_context(request,'jury_overview.html',
        {'exams':exams,
        'lang_id':lang_id,
        'perms':permissions
        })

@login_required
@permission_check
def profile(request,lang_id=1,permissions=None):

    try:
        lang_id = int(lang_id)
        language = Language.objects.get(id=lang_id)
    except:
        raise Http404()

    add_form = AddLanguageForm()
    edit_form = EditLanguageForm(instance=language)

    if request.user.is_staff:
        exams = Exam.objects.all()
    else:
        exams = Exam.objects.filter(staff_only=False)
    
    if request.method == "POST":
        if "editlanguage" in request.POST:
            if not 'admin' in permissions:
                raise PermissionDenied()
            print "in edit"
            form = EditLanguageForm(request.POST,instance=language)
            if form.is_valid():
                lang = form.save()
                #don't want people to remove their own permissions
                if request.user.id not in form.cleaned_data['coordinators']:
                    lang.coordinators.add(request.user)
            edit_form = form
        elif "addlanguage" in request.POST:
            form = AddLanguageForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                lang = Language(name=cd['name'])
                lang.save()
                lang.editors.add(request.user)
                lang.coordinators.add(request.user)
                for exam in exams:
                    exam.languages.add(lang)
                #switch view to new language
                return HttpResponseRedirect('/jury/'+str(lang.id)+'/')
            else:
                add_form = form
        else:
            #unknown form
            raise Http404()
            
    languages = Language.objects.get(id=1).coordinators.all()
    languages = request.user.coordinator_set.all() | request.user.editor_set.all()
    return render_with_context(request,'jury_profile.html',
        {'exams':exams,
        'perms':permissions,
        'languages':languages,
        'addform':add_form,
        'editform':edit_form,
        'lang_id':language.id,
        'language':language
        })


@login_required
@permission_check
def examview(request,exam_id=1,lang_id=1,permissions=None):
    try:
        lang_id = int(lang_id)
        exam_id = int(exam_id)
        if request.user.is_staff:
            exam = Exam.objects.get(id=exam_id)
        else:
            exam = Exam.objects.get(id=exam_id,staff_only=0)
    except:
        raise Http404()

    if request.user.is_staff:
        exams = Exam.objects.all()
    else:
        exams = Exam.objects.filter(staff_only=False)

    categories = exam.get_categorized_status(lang_id)

    return render_with_context(request,'jury_examview.html',
        {'exam':exam,
        'exams':exams,
        'lang_id':lang_id,
        'perms':permissions,
        'categories':categories
        })

@login_required
@permission_check
def questionview(request,exam_id=1,question_position=1,lang_id=1,permissions=None):
    try:
        question_position = int(question_position)
        target_language_id = int(lang_id)
        exam_id = int(exam_id)
        if request.user.is_staff:
            exam = Exam.objects.get(id=exam_id)
        else:
            exam = Exam.objects.get(id=exam_id,staff_only=0)
        language = Language.objects.get(id=target_language_id)
    except: 
        raise Http404()

    question = Question.objects.get(exam__id=exam_id,examquestion__position=question_position)
    if request.user.is_staff:
        exams = Exam.objects.all()
    else:
        exams = Exam.objects.filter(staff_only=False)

    original = question.versionnode_set.filter(language=question.primary_language_id).order_by('-timestamp')[:1]

    versions = question.versionnode_set.filter(language=target_language_id).order_by('-timestamp')[:1]


    if request.method == 'POST':
        print request.POST
        form=JuryQuestionForm(request.POST)
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
                origin_id=cd['orig'],
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
        initial = {"orig":original[0].id}
    else:
        initial = {
            'text':versions[0].text,
            'flag':versions[0].flag,
            'checkout':versions[0].checkout,
            'comment':versions[0].comment,
            'orig':original[0].id
        }

    if 'write' in permissions or 'admin' in permissions:
        form=JuryQuestionForm(initial=initial)
    else:
        form=ViewQuestionForm(initial=initial)

    exam.load_question_status(target_language_id)
    
    if not original:
        return HttpResponse("This question does not yet have a version in the primary language")

    return render_with_context(request,'jury_questionview.html',
        {'exam':exam,
        'lang_id':target_language_id,
        'pos':question_position,
        'status':exam.question_status,
        'exams':exams,
        'original':original[0],
        'question':question,
        'compare':compare,
        'form':form,
        'perms':permissions
    })

@login_required
@permission_check
def students(request,lang_id=1,permissions=None):
	# RB: this will surely need an update

    try:
        lang_id = int(lang_id)
        language = Language.objects.get(id=lang_id)
    except:
        raise Http404()

    if request.user.is_staff:
        exams = Exam.objects.all()
    else:
        exams = Exam.objects.filter(staff_only=False)
    
    for e in exams:
        e.load_question_status(lang_id)
       
    #picker = PickLanguageForm(request.user,lang_id,request,initial={'language':request.path})

    return render_with_context(request,'jury_students.html',
        {'exams':exams,
        'lang_id':lang_id,
        'perms':permissions
        })



@login_required
@permission_check
def xmlquestionview(request,exam_id=1,question_position=1,lang_id=1,permissions=None):
    

    try:
        question_position = int(question_position)
        target_language_id = int(lang_id)
        exam_id = int(exam_id)
        if request.user.is_staff:
            exam = Exam.objects.get(id=exam_id)
        else:
            exam = Exam.objects.get(id=exam_id,staff_only=0)
        language = Language.objects.get(id=target_language_id)
    except: 
        raise Http404()

    question = Question.objects.get(exam__id=exam_id,examquestion__position=question_position)
    if request.user.is_staff:
        exams = Exam.objects.all()
    else:
        exams = Exam.objects.filter(staff_only=False)

    original = question.versionnode_set.filter(language=question.primary_language_id).order_by('-timestamp')[0]

    try:
        translation = question.versionnode_set.filter(language=target_language_id).order_by('-timestamp')[0]
    except:
        translation = None

    if request.method == "POST":

        #request.POST = utils.iboclean(request.POST)
        #print "cleaned!",request.POST

        if not ('write' in permissions or 'admin' in permissions):
            raise PermissionDenied()
       
        form=JuryQuestionForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            print cd 
        else:
            print request.POST
            print form.errors
        #populate juryform
        #replace known tags
        #strip remaining html
 
        rating = None
        if "rating" in request.POST:
            rating = request.POST["rating"]

        oxml = QMLquestion(original.text)
        clean_post = utils.iboclean(request.POST)
        print "CLEAN",clean_post
        oxml.update(clean_post)
        if not translation:
            vid = 1
        else:
            vid = translation.version+1

        v = VersionNode(
            question_id=question.id,
            language_id=target_language_id,
            version=vid,
            rating=rating,
            text=oxml.zackzack(),
            flag=cd['flag'],
            checkout=cd['checkout'],
            comment=cd['comment']
        )
        v.save()

        tr = Translation(
            language=v.language,
            origin_id=cd['orig'],
            target=v
        )
        tr.save()
        return redirect(request.path + "?success") 
   
    if translation is None:
        initial = {'orig':original.id}
    else:
        initial = {
            'text':'',
            'flag':translation.flag,
            'checkout':translation.checkout,
            'comment':translation.comment,
            'orig':original.id
        }
    
    if 'write' in permissions or 'admin' in permissions:
        form=JuryQuestionForm(initial=initial)
        ro = ""
    else:
        form=ViewQuestionForm(initial=initial)
        ro = "readonly"

    exam.load_question_status(target_language_id)

    struct = make_xml_form(original,translation)
    cmt = ""
    tv = 0
    if translation is not None:
        cmt = translation.comment
        tv = translation.version
    return render_with_context(request,'jury_test.html',
        {'exam':exam,
        'lang_id':target_language_id,
        'pos':question_position,
        'status':exam.question_status,
        'exams':exams,
        'form':form,
        'question':question,
        'struct':struct,
        'comment':original.comment,
        'versions':{'orig':original.version,'trans':tv},
        'perms':permissions,
        'readonly': ro
    })


#puts together the text obtained from 
def make_xml_form(original,translation):
    oxml = QMLquestion(original.text)
    texts = oxml.get_texts_nested()
    if translation is not None:
        print "translation is not none"
        txml = QMLquestion(translation.text)
        oxml.update(txml.get_data())
        forms = oxml.get_texts_nested()
    else:
        print "translation is none"
        oxml.update({})
        forms = oxml.get_texts_nested()
    #oxml.update(txml.get_data())
    #forms = oxml.get_forms_nested()
    print "txt",texts,"FOOOOOOOOOOOOR",forms
    return zipem(texts,forms)
    
    
def zipem(texts,forms):
    try:
        assert len(texts) == len(forms)
    except:
        print len(texts),len(forms)
        print texts," UAUAUAUA", forms
        raise Exception("yep")
    rt = []
    for i in xrange(len(texts)):
        if not isinstance(texts[i]["data"],unicode) and not isinstance(texts[i]["data"],str): #it's a list
            #print type(texts[i]["data"])
            data = zipem(texts[i]["data"],forms[i]["data"])
            texts[i].update({"data":data})
            rt.append(texts[i])
        else:
            texts[i].update({"form":utils.prep_for_display(forms[i]["data"])})
            texts[i]["data"] = utils.prep_for_display(texts[i]["data"])
            rt.append(texts[i])

    return rt




