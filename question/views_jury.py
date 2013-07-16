from uuid import uuid4
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required
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
from ibo2013.question import views_staff as staffview

 
@permission_required('question.is_jury')
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

@permission_required('question.is_jury')
@permission_check
def profile(request,lang_id=1,permissions=None):

    try:
        lang_id = int(lang_id)
        language = Language.objects.get(id=lang_id)
    except:
        raise Http404()

    add_form = AddLanguageForm()
    edit_form = EditLanguageForm()
    ctr = CategoryTranslation.objects.filter(language=language).order_by("category")
    #print ctr
    init = {}
    for c in ctr:
        init["f"+str(c.category_id)] = c.text
    #print init
    cf = CatTransForm(initial=init)

    if request.user.is_staff:
        exams = Exam.objects.all()
    else:
        exams = Exam.objects.filter(staff_only=False)
    
    if request.method == "POST":
        if "editlanguage" in request.POST:
            #print request.POST
            #print 'ok'
            if not 'admin' in permissions:
                raise PermissionDenied()
            form = EditLanguageForm(request.POST)
            #print form.is_bound
            if form.is_valid():
                cd = form.cleaned_data
                dlg = cd['dlg']
                members = dlg.members.all()
                rt = []
                for m in members:
                    if "Jury" in m.groups.values_list("name",flat=True):
                        rt.append(m.id)
                language.editors.add(*rt)

                return redirect(request.path)
                #don't want people to remove their own permissions
                #if request.user.id not in form.cleaned_data['coordinators']:
                #    lang.coordinators.add(request.user)
            edit_form = form
        elif "addlanguage" in request.POST:
            form = AddLanguageForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                lang = Language(name=cd['name'])
                lang.save()
                members = request.user.delegation_set.all()[0].members.all()#includes students, but who cares
                rt = []
                for m in members:
                    if "Jury" in m.groups.values_list("name",flat=True):
                        rt.append(m.id)
                lang.editors.add(*rt)
                lang.coordinators.add(request.user)
                for exam in exams:
                    exam.languages.add(lang)
                #switch view to new language
                return HttpResponseRedirect('/jury/'+str(lang.id)+'/')
            else:
                add_form = form
        elif "translate_cat" in request.POST:
            if not ('edit' in permissions or 'admin' in permissions):
                raise PermissionDenied()
            f = CatTransForm(request.POST)
            if f.is_valid():
                cd = f.cleaned_data
                for c in cd:
                    ct,created = CategoryTranslation.objects.get_or_create(category_id=int(c[1:]),language=language)
                    ct.text = cd[c]
                    ct.save()
                return redirect(request.path)
            else:
                print "error"
        else:
            #unknown form
            raise Http404()
            
    languages = request.user.editor_set.all()
    languages2 = request.user.coordinator_set.all()
    access = language.editors.all().order_by('first_name','last_name')


    return render_with_context(request,'jury_profile.html',
        {'exams':exams,
        'perms':permissions,
        'access':access,
        'languages':languages,
        'languages2':languages2,
        'addform':add_form,
        'editform':edit_form,
        'lang_id':language.id,
        'language':language,
        'cf':cf
        })


@permission_required('question.is_jury')
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

    if request.method == "POST":
        x = dict(request.POST.iterlists())
        return staffview.print_questions(x['pdfselect'],lang_id,exam_id)


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


@permission_required('question.is_jury')
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
       
    return render_with_context(request,'jury_students.html',
        {'exams':exams,
        'lang_id':lang_id,
        'perms':permissions
        })


@permission_required('question.is_jury')
@permission_check
def vote(request,lang_id=1,permissions=None):
	# RB: this will surely need an update
	# * Add delegation check (hidden parameter 'delegation' in template)
	# * Add flag to know if there is an active vote going on ('voteactive' in template)
	# * If something has already been submit, send it ('submitted' in template)
	#
	# Staff view needs to be made... with automatic update of votings
	
    if request.user.is_staff or request.user.is_superuser:
        delegation = Delegation.objects.get(name="Exam_Staff")
    else:
        delegation = request.user.delegation_set.all()[0]
    voteactive=False 
    ovo = VotingRound.objects.filter(active=True,closed=False).order_by('-id')
    if len(ovo) > 0:
        ovo = ovo[0]
        voteactive=True

    if request.method == "POST":
        if "vote" in request.POST:
            v,c = Vote.objects.get_or_create(delegation=delegation,vround=ovo)
            if not request.POST["vote"] in ['yes','no','abstain']:
                raise Http404()#not really right, but hey...
        	v.answer = request.POST['vote']
            if request.POST['vote'] == "abstain":
                v.answer = "abstain"
            if request.POST['vote'] == "yes":
                v.answer = "yes"
            if request.POST['vote'] == "no":
                v.answer = "no"
            v.save()

            return redirect(request.path+"?success")
        else:
            #unknown form
            raise Http404()
    
    if request.user.is_staff:
        exams = Exam.objects.all()
    else:
        exams = Exam.objects.filter(staff_only=False)
    
    v = Vote.objects.filter(delegation=delegation,vround=ovo)    
    if v.count() > 0:
        submitted = v[0].answer
    else:
        submitted = ''    
    languages = Language.objects.get(id=1).coordinators.all()
    languages = request.user.coordinator_set.all() | request.user.editor_set.all()
    return render_with_context(request,'jury_vote.html',
        {'voteactive':voteactive,
        'ovo':ovo,
        'submitted':submitted,
        'lang_id':lang_id,
        'perms':permissions,
        'exams':exams
        })

@login_required
@permission_check
def xmlquestionview(request,exam_id=1,question_position=1,lang_id=1,from_lang_id=None,permissions=None):
    actual_path = request.path 
    if from_lang_id is None:
        from_lang_id = request.session.get("from_lang_id",1)
        actual_path = request.path+str(from_lang_id)+"/" 
        #print actual_path
    else:
        request.session["from_lang_id"] = int(from_lang_id)

    try:
        question_position = int(question_position)
        target_language_id = int(lang_id)
        exam_id = int(exam_id)
        if request.user.is_staff:
            exam = Exam.objects.get(id=exam_id)
        else:
            exam = Exam.objects.get(id=exam_id,staff_only=0)
        language = Language.objects.get(id=target_language_id)
        from_lang = Language.objects.get(id=int(from_lang_id))
    except: 
        raise Http404()

    question = Question.objects.get(exam__id=exam_id,examquestion__position=question_position)
    if request.user.is_staff:
        exams = Exam.objects.all()
    else:
        exams = Exam.objects.filter(staff_only=False)
    
    fls = PickLanguageForm(request.user,lang_id,request,
            initial={'language':actual_path},
            languages = None,#Language.objects.filter(id__in=[1,25]),
            realpath = actual_path,
            pos = -2
        )

    try:
        original = question.versionnode_set.filter(language=from_lang,committed=1).order_by('-version')[0]
    except:
        exam.load_question_status(target_language_id)
        return render_with_context(request,'jury_test.html',
        {'sorryaboutthat':True,
        'exam':exam,
        'from_language_switch':fls,
        'lang_id':target_language_id,
        'pos':question_position,
        'status':exam.question_status,
        'exams':exams,
        'question':question,
        'perms':permissions,
    })   
    #not translating from english means we need to refer to the original english version
    outdated = False
    if from_lang.id != question.primary_language_id:
        tr = Translation.objects.get(target=original)
        
        root_original_version = tr.origin.version
        cv = question.versionnode_set.filter(language=1,committed=1).order_by('-version')[0]
        if tr.origin.version <  cv.version:
            outdated = True
            #print tr.target
            #print cv
            #print cv,">",tr.origin
    else:
        #print "original",original
        #cv = question.versionnode_set.filter(language=1,committed=1).order_by('-version')[0]
        #print "current",cv
        #translation = question.versionnode_set.filter(language=target_language_id).order_by('-version')[0]
        #myo = Translation.objects.get(target=translation)
        #print "my original",myo
        #trans_from_version = myo.origin.version
        root_original_version = original.version
    try:
        translation = question.versionnode_set.filter(language=target_language_id).order_by('-version')[0]
        myo = Translation.objects.get(target=translation)
        trans_from_version = myo.origin.version
    except:
        trans_from_version = "NA"
        translation = None

    if request.method == "POST":

        #request.POST = utils.iboclean(request.POST)

        if not ('write' in permissions or 'admin' in permissions):
            raise PermissionDenied()
       
        form=JuryQuestionForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
        else:
            cd = {'flag':0,'checkout':0,'comment':'',rating:0,'orig':1}

        #print "formvalid",form.is_valid()
        #print "cd",form.cleaned_data

        oxml = QMLquestion(original.text)
        clean_post = utils.iboclean(request.POST)
        oxml.update(clean_post)
        if not translation:
            vid = 1
        else:
            vid = translation.version+1

        v = VersionNode(
            question_id=question.id,
            language_id=target_language_id,
            version=vid,
            rating=cd['rating'],
            text=oxml.zackzack(),
            flag=cd['flag'],
            checkout=cd['checkout'],
            comment=cd['comment'],
            committed=True
        )
        v.save()
        if not v.language == question.primary_language_id:
            ori_blaaaaah = VersionNode.objects.get(question=question,language=1,version=cd['orig'])
            tr = Translation(
                language=v.language,
                origin=ori_blaaaaah,
                target=v
            )
            tr.save()
            #print "tr",tr
        if "nextsubmit" in request.POST:
            ps = request.path.split("/")
            ps[-3] = str(question_position + 1)
            nextpath = "/".join(ps)
            return redirect(nextpath)
        else:
            return redirect(request.path + "?success") 

    if translation is None:
        initial = {'orig':original.id,'rating':0}
    else:
        initial = {
            'text':'',
            'flag':translation.flag,
            'checkout':translation.checkout,
            'comment':translation.comment,
            'rating':translation.rating,
            'orig':root_original_version
        }
    
    if 'write' in permissions or 'admin' in permissions:
        form=JuryQuestionForm(initial=initial)
        ro = ""
        dis = False
    else:
        form=ViewQuestionForm(initial=initial)
        ro = "readonly"
        dis = True

    exam.load_question_status(target_language_id)

    oqml = QMLquestion(original.text.encode('utf-8'))
    try:
    
        #checkout = 1 or not??
        tr_checkout = question.versionnode_set.filter(language=target_language_id).order_by('-version')[0]
        if from_lang_id == question.primary_language_id:
            previous = tr_checkout.translation_target.all()[0].origin
        else:
            #need to do a little bit of magic here...
            previous = tr_checkout.translation_target.all()[0].translation_origin.filter(language=from_lang_id).order_by('-version')[0]
        pqml = QMLquestion(previous.text.encode('utf-8'))
        #oqml.diff(pqml.get_data())
    except:
        pass


    struct = make_xml_form(oqml,translation)
    cmt = ""
    tv = 0
    if translation is not None:
        cmt = translation.comment
        tv = translation.version
    #print "root original version",root_original_version
    return render_with_context(request,'jury_test.html',
        {'sorryaboutthat':False,
        'exam':exam,
        'lang_id':target_language_id,
        'pos':question_position,
        'status':exam.question_status,
        'exams':exams,
        'form':form,
        'from_language_switch':fls,
        'lang_id':target_language_id,
        'rating':initial['rating'],
        'question':question,
        'struct':struct,
        'comment':original.comment,
        'versions':{'orig':root_original_version,'trans':tv},
        'perms':permissions,
        'readonly': ro,
        'disabled': dis,
        'outdated':outdated,
        'trans_from_version':trans_from_version
    })


#puts together the text obtained from original (as qml) and translation (Vnode)
def make_xml_form(oxml,translation):
    texts = oxml.get_texts_nested()
    if translation is not None:
        txml = QMLquestion(translation.text.encode('utf-8'))
        oxml.update(txml.get_data())
        forms = oxml.get_texts_nested()
    else:
        oxml.update({})
        forms = oxml.get_texts_nested()
    #oxml.update(txml.get_data())
    #forms = oxml.get_forms_nested()
    return zipem(texts,forms)
    
    
def zipem(texts,forms):
    #print "texts=",texts
    #print "-----"
    #print "forms=",forms
    try:
        assert len(texts) == len(forms)
    except:
        raise Exception("yep {0} != {1}".format(len(texts),len(forms)))
    rt = []
    for i in xrange(len(texts)):
        if not isinstance(texts[i]["data"],unicode) and not isinstance(texts[i]["data"],str): #it's a list
            print "tags=",texts[i]['tag']," AND ",forms[i]['tag']
            data = zipem(texts[i]["data"],forms[i]["data"])
            texts[i].update({"data":data})
            rt.append(texts[i])
        else:
            texts[i].update({"form":utils.prep_for_display(forms[i]["data"])})
            texts[i]["data"] = utils.prep_for_display(texts[i]["data"])
            rt.append(texts[i])

    return rt



@permission_check
@permission_required('question.is_jury')
def practical(request,lang_id=1,permissions=None):
    try:
        language = Language.objects.get(id=lang_id)
    except:
        raise Http404()

    if request.user.is_staff:
        exams = Exam.objects.all()
    else:
        exams = Exam.objects.filter(staff_only=False)
    staffd = Delegation.objects.get(name='Exam_Staff')
    official_files = PracticalExamFile.objects.filter(delegation=staffd).order_by('name')
    practicals = PracticalExam.objects.all().order_by('position')
    if request.user.is_staff or request.user.is_superuser:
        delegation = Delegation.objects.get(name="Exam_Staff")
    else:
        delegation = request.user.delegation_set.all()[0]
    students = Student.objects.filter(delegation=delegation)
    examfiles = PracticalExamFile.objects.filter(delegation=delegation).order_by('-version')
    assignments = PracticalAssignment.objects.filter(student__in=students)


    finalized = True
    if len(assignments) == 0:
        finalized = False
    for a in assignments:
        if a.finalized == False:
            finalized=False

    if request.user.is_staff or request.user.is_superuser:
        finalized = False

    if request.method == 'POST':
        if "upload" in request.POST:
            uploadform = UploadPracticalForm(request.POST,request.FILES)
            if uploadform.is_valid():
                name = uploadform.cleaned_data['name']
                if len(name) < 3:
                    name = request.FILES['pfile'].name
                filename = delegation.name+"_"+name+"_"+request.FILES['pfile'].name
                try:
                    pe = PracticalExamFile.objects.get(name=name,delegation=delegation)
                    pe.filename = filename
                    pe.owner = request.user                
                except:
                    pe = PracticalExamFile(name=name,filename=filename,owner=request.user,delegation=delegation)
                pe.save()
                pe.handle_uploaded_file(request.FILES['pfile'])
                pe.save()
                return redirect(request.path+"?success")
            else:
                init = {}
                for a in assignments:
                    init["{0}__{1}".format(a.student_id,a.practical_exam_id)] = a.practical_exam_file_id
                assignform = AssignPracticalForm(students=students,practicals=practicals,initial=init)
                #create new PracticalExamFile, for this delegation
        elif "delete" in request.POST:
            pe = PracticalExamFile.objects.get(id=int(request.POST['file']))
            if pe.delegation == delegation:
                pe.delete_file()
                pe.delete()
                return redirect(request.path+"?success")

        elif "assign" in request.POST:
            assignform = AssignPracticalForm(request.POST,students=students,practicals=practicals)
            if assignform.is_valid():
                cd = assignform.cleaned_data
                for k in cd:
                    (s,p) = k.split("__")
                    assignment, created = PracticalAssignment.objects.get_or_create(student_id=s,practical_exam_id=p)
                    assignment.practical_exam_file_id = cd[k]
                    assignment.save()
                return redirect(request.path+"?success")

        elif "finalize" in request.POST:
            pa = PracticalAssignment.objects.filter(student__in=students)
            if len(students)*PracticalExam.objects.all().count() == pa.count():
                for s in pa:
                    s.finalized = True
                    s.save()
            else:
                pass
            return redirect(request.path+"?success")
        else:
            raise Http404()
    else:
        init = {}
        for a in assignments:
            init["{0}__{1}".format(a.student_id,a.practical_exam_id)] = a.practical_exam_file_id
        uploadform = UploadPracticalForm()
        assignform = AssignPracticalForm(students=students,practicals=practicals,initial=init)


    return render_with_context(request,'jury_practical.html',
        {'lang_id':lang_id,
        'finalized':finalized,
        'uploadform':uploadform,
        'assignform':assignform,
        'exams':exams,
        'practicals':official_files,
        'assignments':assignments,
        'delegation':delegation,
        'students':students,
        'perms':permissions,
        'language':language,
        'examfiles':examfiles})
   

    def find_real_origin():
        pass 
