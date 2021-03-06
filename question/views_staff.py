from django.shortcuts import render_to_response, redirect
from django.core.servers.basehttp import FileWrapper
from django.http import Http404, HttpResponse, HttpResponseRedirect
from ibo2013.question.models import *
from ibo2013.question.forms import *
from ibo2013.question import utils
from django.db.models import Count
from django.db import connections
from django.template import RequestContext
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from ibo2013.question import qml
from django.db.models import Q
from django.utils import safestring
from xml.etree import ElementTree as et
import base64
import os

@login_required
@staff_member_required
def view_exam(request,exam_id):
    try:
        exam_id = int(exam_id)
        exam = Exam.objects.get(id=exam_id)
    except:
        raise Http404()
    
    if request.method == 'POST':
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

    versions = question.versionnode_set.all().order_by('-version')
    return render_to_response('question_overview.html',{'question':question,'versions':versions})




@login_required
@staff_member_required
def view_question(request,qid=None,mode="xml"):
    mode="xml" #very nice...
    try:
        question_id = int(qid)
        question = Question.objects.get(id=question_id)
    except:
        raise Http404()

    #todo: change this to include only the last version
    if "lang_id" in request.GET:
        chosen_lang_id = request.GET["lang_id"]
    else:
        chosen_lang_id = question.primary_language_id
    versions = question.versionnode_set.filter(language=chosen_lang_id).order_by('-version')[:1]

    if request.method == 'POST':
        if len(versions) == 0:
            vnum = 1
            lang_id = chosen_lang_id
        else:
            vnum = versions[0].version + 1
            lang_id = versions[0].language_id            
            
        if "reident" in request.POST:
            xmlq = qml.QMLquestion(versions[0].text)
            xmlq.reassign_identifiers(question.id) 
            v = VersionNode(question_id=question.id,language_id=lang_id,version=vnum,text=xmlq.zackzack())
            v.save()
            return redirect(request.path) #POST,GET redirect for instant reload   

        if "revert" in request.POST:
            vnodes = VersionNode.objects.filter(question=question,language=chosen_lang_id).order_by('-version')
            for v in vnodes:
                if not v.committed:
                    v.delete()
                else:
                    #we're done, return
                    return redirect(request.path)
        else:
            if mode == "normal":
                xmlq = qml.QMLquestion(versions[0].text)
                form = QMLform(request.POST,qml=xmlq)
                if form.is_valid():
                    xmlq.update(form.cleaned_data)
                   
                    v = VersionNode(question_id=question.id,language_id=lang_id,version=vnum,text=xmlq.zackzack())
                    v.save()
                    versions = list(versions)
                    versions.append(v)   
                    
                    return redirect(request.path) #POST,GET redirect for instant reload   
                else:
                    pass
            elif mode == "xml": 
                form = EditQuestionForm(request.POST)
                if form.is_valid():
                    cd = form.cleaned_data
                    if len(versions) == 0:
                        vnum = 1
                        lang_id = chosen_lang_id
                    else:
                        vnum = versions[0].version + 1
                        lang_id = versions[0].language_id            

                    xmlq = qml.QMLquestion(cd['text'])

                    #order is important! parse figure first, then assign id
                    xmlq.parse_figures() #inserts variable fields for figure
                    xmlq.assign_initial_id(question.id) #assigns unique id where id=""

                    v = VersionNode(question_id=question.id,language_id=lang_id,version=vnum,text=xmlq.zackzack(pretty=False),comment=cd['comment'],flag=cd['flag'],checkout=cd['checkout'],committed=cd['commit'])
                    v.save()
                    versions = list(versions)
                    versions.append(v)   
                    
                    return redirect(request.path) #POST,GET redirect for instant reload   
            else:
                raise ValueError("no such view mode: >" + str(mode)+"<")
        
    #request method is not POST, no form was submitted
    else:
        if len(versions) > 0 and mode == "normal":
            try:
                xmlq = qml.QMLquestion(versions[0].text)
                form = QMLform(qml=xmlq)
            except Exception as e:
            #    if versions[0].text.startswith('<question'):
            #        #this should probably be xml, raise exception
            #        raise e
            #    else:
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

    fig_form = FigureChoiceForm()

    return render_to_response('staff_questionview.html',
        {'question':question,
        'versions':versions,
        'vnode':versions[0],
        'form':form,
        'compare':compare,
        'viewmode':mode,
        'lang_id':chosen_lang_id,
        'fig_form':fig_form})
        
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
                pass
        if "update" in request.POST:
            try:
                instance=QuestionCategory.objects.get(id=int(request.POST['cat_id']))
                f = EditCategoryForm(request.POST,instance=instance)
                if f.is_valid():
                    f.save()
                    return redirect("/staff/categories?success")
                else:
                    errors = form.errors
            except:
                pass
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
        orig = trans[0]
        if len(trans) == 1:
            frm = TranslateCategoryForm()
        else:
            frm = TranslateCategoryForm(instance=trans[1])
            
        objs.append({"orig":orig,"form":frm})

    cf = CatTransForm(cats=cats)

    return render_to_response('staff_categories_trans.html',{'objs':objs,'catform':cf})


@staff_member_required
def upload_figure(request):
    if request.method == 'POST':
        if "delete" in request.POST:
            try:
                f = Figure.objects.get(pk=int(request.POST["img_id"]))
                f.delete()
            except:
                raise Http404()

            return HttpResponseRedirect(request.path + "?success")


        form = UploadFigureForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['name'] == "":
                cd['name'] = request.FILES['imgfile'].name
            process_uploaded_figure(request.FILES['imgfile'],cd['name'],cd['description'])
            return HttpResponseRedirect(request.path + "?success")
    else:
        form = UploadFigureForm()

    images = Figure.objects.all().order_by("name")
    return render_to_response('staff_uploadfigure.html',{'form':form,'images':images})

def process_uploaded_figure(f,fname,descr):
    #on success, insert picture in database
    xml = f.read()
    et.register_namespace("","http://www.w3.org/2000/svg")
    fsvg = et.fromstring(xml)
    tags = find_figure_tags(fsvg)
    var = u'<replace>'
    for (el_id,txt) in tags:
        var += u'<textarea id="" ibotag="{0}">{1}</textarea>\n'.format(el_id,unicode(txt))
    var += u'</replace>'
    fig = Figure(name=fname,description=descr,svg=et.tostring(fsvg),var=unicode(var))
    fig.save()


def find_figure_tags(svg_el):
    rt = []
    if "id" in svg_el.attrib:
        sid = svg_el.attrib["id"]
        if sid.startswith("IBOtranslation"):
            if len(svg_el) == 1:
                if len(svg_el[0]) > 0:
                    raise QMLParseError("tspan Element shouldn't have any subelements  at " + sid + " " + et.tostring(svg_el))
                rt.append((sid,svg_el[0].text))
                svg_el[0].text = hex(hash(sid))
            elif len(svg_el) == 0:
                rt.append((sid,svg_el.text))
                svg_el.text = hex(hash(sid))
            else:
                raise QMLParseError("IBOtranslation tagged text element can only have one tspan "+ et.tostring(svg_el))

    for child in svg_el:
        rt.extend(find_figure_tags(child))


    return rt

class QMLParseError(Exception):
    pass

#@staff_member_required
@login_required
def view_image(request,fname="",qid=None,lang_id=1,version=None):
    #if (not request.user.is_staff) and (int(exam_id) not in [1,2]):
    #    raise PermissionDenied() #TODO: just a hack to keep people out
    
    try:
        img = Figure.objects.get(name=fname)
    except:
        raise Http404()

    svg = img.svg
    if qid is None:
        replace = et.fromstring(img.var.encode('utf-8'))
    else:
        try:
            q = Question.objects.get(id=int(qid))
        except:
            raise Http404()
        try:
            if version is None:
                vn = q.versionnode_set.filter(committed=1,language=lang_id).order_by('-version')[0]
            else:
                vn = q.versionnode_set.get(language=lang_id,version=version)
        except:
            raise Http404()
        search = ".//figure[@imagefile='{0}']/textarea".format(fname)
        replace = et.fromstring(vn.text.encode('utf-8')).findall(search)
    for r in replace:
        svg = svg.replace(hex(hash(r.attrib['ibotag'])),r.text)

    resp = HttpResponse(svg,mimetype="image/svg+xml")
    #resp['cache-control'] = 'private'
    return resp


@staff_member_required
def get_pdf(request,exam_id,question_position,lang_id=1):
 
    try:
        question_position = int(question_position)
        exam_id = int(exam_id)
        question = Question.objects.get(exam__id=exam_id,examquestion__position=question_position)
        vnode = question.versionnode_set.filter(language=lang_id).order_by('-version')[0]
    except: 
        raise Http404()

    xmlq = qml.QMLquestion(vnode.text.encode("utf-8"))
    xmlq.inline_image()
    txt = xmlq.zackzack()
    #for i in xrange(9): #ugly hack because TCPDF svg renderer is  incompetent
    #    txt = txt.replace("ns{0}:".format(i),"")
    #txt = txt.replace("rdf:","")
    return HttpResponse(txt,content_type="text/plain")

@staff_member_required
def print_exam(request,exam_id,lang_id=1):
    try:
        exam = Exam.objects.get(id=int(exam_id))
        language = Language.objects.get(id=int(lang_id))
    except:
        raise Http404()


    questions = ExamQuestion.objects.filter(exam=exam).order_by("position")
    exam_xml = print_question_objects(questions,lang_id,exam_id)
    return HttpResponse(exam_xml,content_type="text/plain")
    #TODO: implement proper pdf printing

    filename = "{0}_{1}_{2}.pdf".format(exam.name,language.name,request.user.id)
    utils.xml2pdf(exam_xml,filename,images=True)
    path = 'xml2pdf/output/{0}'.format(filename)
    wrapper = FileWrapper(file(path))
    response = DeleteFileAfterResponse(wrapper,content_type='application/pdf',filename=path)
    response['Content-Length'] = os.path.getsize(path)
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response

def simpleprint(request,qlist,lang_id=1,exam_id=3):
    try:
        questions = ExamQuestion.objects.filter(id__in=[int(x) for x in qlist]).order_by("position")
        #question_position = int(question_position)
        exam_id = int(exam_id)
        exam = Exam.objects.get(id=exam_id,staff_only=0)
        language = Language.objects.get(id=lang_id)
        num_questions = ExamQuestion.objects.filter(exam=exam_id).count()
    except:
        raise Http404()

    qarray = []
    for eq in questions:
        question = eq.question
        flag = ExamFlags.objects.filter(user=request.user,question=eq).count() > 0
        
        sol = ExamAnswers.objects.get(user=303,question=eq)
        this_solution = [(3,sol.answer1),(4,sol.answer2),(5,sol.answer3),(6,sol.answer4)] 

        try:
        	trans_category = CategoryTranslation.objects.get(category=eq.category,language=lang_id)
        except:
        	trans_category = CategoryTranslation.objects.get(category=eq.category,language=1)

        try:
            a = ExamAnswers.objects.get(user=request.user,question=eq)
            this_answer = [(3,a.answer1),(4,a.answer2),(5,a.answer3),(6,a.answer4)] 
        except:
            this_answer = [(3,None),(4,None),(5,None),(6,None)]
        
        try:
            en_vnode = question.versionnode_set.filter(language=1).order_by('-version')[0]
            vnode = question.versionnode_set.filter(language=language.id).order_by('-version')[0]
            xmlq = qml.QMLquestion(vnode.text)
            struct = xmlq.get_texts_nested(prep=True)
            
            qarray.append(
                {'struct':struct,
                'available':True,
                'vnode':vnode,
                'pos':eq.position,
                'question':question,
                'eq':eq,
                'answers':this_answer,
                'solution':this_solution,
                'trans_category':trans_category,
                'official_commentary':safestring.mark_safe(en_vnode.comment),
                'flag':flag,
                })

        except: 

            qarray.append(
                {'available':False,
                'pos':question_position,
                'question':question,
                'eq':eq,
                'flag':flag,
                'answers':this_answer,
                'solution':this_solution,
                'trans_category':trans_category,
                'official_commentary':safestring.mark_safe(en_vnode.comment),
                })

    langs = Language.objects.filter(id__in=[1,2])
    picker = PickLanguageForm(request.user,lang_id,request,languages = langs,initial={'language':request.path})        

    if not request.user.username.startswith("test"):
        #delegation = request.user.delegation_set.all()[0]
        #picker = PickLanguageForm(request.user,lang_id,request,languages=delegation.exam_languages.all(),initial={'language':request.path})        
        picker = PickLanguageForm(request.user,lang_id,request,initial={'language':request.path})        
    return render_to_response('jury_printview.html',
        {
        'exam_id':exam_id,
        'lang_id':lang_id,
        'language':language,
        'user':request.user,
        'qarray':qarray,
        'num_questions':num_questions,
        'lang_picker':picker
    })




# don't call directly! use only through other view.
def print_questions(request,qlist,lang_id=1,exam_id=3):

    if len(qlist) > 100:
        return HttpResponse("Please download at most 100 questions at once. Sorry for the inconvenience, we hope to be able to remove this limitation at a later stage.",content_type="text/plain")
    show_images = False
    if len(qlist) == 1:
        show_images = True
    try:
        exam = Exam.objects.get(id=int(exam_id))
        language = Language.objects.get(id=int(lang_id))
    except:
        raise Http404()

    questions = ExamQuestion.objects.filter(id__in=[int(x) for x in qlist]).order_by("position")
    exam_xml = print_question_objects(questions,lang_id,exam_id)
    return HttpResponse(exam_xml,content_type="text/plain")
    #TODO: implement proper pdf printing

    filename = "{0}_{1}_{2}.pdf".format(exam.name,language.name,request.user.id)
    utils.xml2pdf(exam_xml,filename,show_images)
    path = 'xml2pdf/output/{0}'.format(filename)
    wrapper = FileWrapper(file(path))
    response = DeleteFileAfterResponse(wrapper,content_type='application/pdf',filename=path)
    response['Content-Length'] = os.path.getsize(path)
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response

def print_question_objects(questions,lang_id=1,exam_id=3):        

    #return HttpResponse("Sorry, this feature is not working at the moment. We hope to have it working again soon!",content_type="text/plain")


    root = et.Element("exam")
    root.attrib["name"] = "print_exam_test"
    for q in questions:
        try:
            vnode = q.question.versionnode_set.filter(language=lang_id).order_by('-version')[0]
            target_vid = vnode.version
        except:
            target_vid = 0
            vnode = q.question.versionnode_set.filter(language=1,committed=True).order_by('-version')[0]
        xmlq = qml.QMLquestion(vnode.text.encode("utf-8"))
        #xmlq.inline_image()
        xmlq.xml.attrib["info"] = "{0}_{1}_L{2}".format(vnode.version,target_vid,lang_id)
        xmlq.xml.attrib['position'] = str(q.position)
        comment = et.Element("comment")
        comment.text = vnode.comment#.encode("utf-8")
        #comment.text = base64.b64encode(vnode.comment.encode("utf-8"))
        #TODO: re-encode in utils.xml2pdf
        xmlq.xml.append(comment)
        root.append(xmlq.xml)

    return et.tostring(root,encoding='utf-8')


"""
Http Response class that removes a temporary file created for the response
"""
class DeleteFileAfterResponse(HttpResponse):
    def __init__(self,*args,**kwargs):
        self.filename = kwargs.pop('filename')
        super(DeleteFileAfterResponse,self).__init__(*args,**kwargs)

    def close(self):
        os.remove(self.filename)
        pass

@staff_member_required
def discussion(request,exam_id,question_position):

    #if not request.user.is_staff and int(exam_id) > 2:
    #    raise PermissionDenied()

    try:
        question_position = int(question_position)
        exam_id = int(exam_id)
        question = Question.objects.get(exam__id=exam_id,examquestion__position=question_position)
        vnode = question.versionnode_set.filter(language=1).order_by('-version')[0]
        orig = question.versionnode_set.filter(language=1,committed=1).order_by('-version')[0]
    except: 
        raise Http404()
    
    original = qml.QMLquestion(orig.text)
    xmlq = qml.QMLquestion(vnode.text)
    struct = xmlq.get_texts_nested(prep=True,compare_to=original)

    counter = 0
    if "reload" in request.GET:
        counter = request.GET['reload']

    return render_to_response('staff_discussion.html',{'question':question,'question_position':question_position,'vnode':vnode,'struct':struct,'counter':counter})



@staff_member_required
def practical(request):
    if request.method == 'POST':
        finals = {}
        prints = {}
        for k in request.POST:
            sp = k.split('-')
            if sp[0] == u"printed":
                if len(sp) == 3 and "-".join(sp[:2]) not in request.POST:
                    prints[sp[1]] = False
                if len(sp) == 2:
                    prints[sp[1]] = True
            elif sp[0] == u"finalized":
                if len(sp) == 3 and "-".join(sp[:2]) not in request.POST:
                    finals[sp[1]] = False
                if len(sp) == 2:
                    finals[sp[1]] = True
        
            else:
                pass
        for f in finals:
            a = PracticalAssignment.objects.get(id=int(f))
            a.finalized = finals[f]
            a.printed = prints[f]
            a.save()            

        return redirect(request.path)
    
    assignments = PracticalAssignment.objects.all().order_by('printed','-finalized','student')
    return render_to_response('staff_practical.html',{
        #'practicals':practicals,
        'assignments':assignments
        })


@staff_member_required
def vote(request):
    if request.method == 'POST':
        if "round" in request.POST:
            r = VotingRound.objects.get(id=int(request.POST["round"])) 
            form = StaffVoteForm(request.POST,instance=r)
        else:
            form = StaffVoteForm(request.POST)
        if form.is_valid():
            form.save()   
            return redirect(request.path+'?success')
 
    vr = VotingRound.objects.all().order_by('-id')
    dl = Delegation.objects.all().order_by('name')
    current = None
    votes = []
    vnum = 0
    if len(vr) > 0:
        current = vr[0]

        votes = Vote.objects.filter(vround=current.id).order_by('delegation')
        vnum = votes.count()

    stats = {'yes':0,'no':0,'abstain':0,'noanswer':dl.count()-vnum-6}
    do = []
    for d in dl:
        if d.name in ["Exam_Staff","Test country", "Malaysia","Ireland","France","Portugal"]:
            continue
        a = ''
        for v in votes:
            if v.delegation == d:
                a = v.answer
                stats[v.answer] += 1
                break;
        do.append({'d':d,'v':a})

    forms = []
    for r in vr:
        forms.append({'frm':StaffVoteForm(instance=r),'id':r.id})

    newform = StaffVoteForm()

    return render_to_response('staff_vote.html',{
        'current':current,
        'rounds':vr,
        'votes':do,
        'forms':forms,
        'newform':newform,
        'stats':stats,
        'active':(current is not None) and current.active and (not current.closed)
    }
)

@staff_member_required
def score_practical(request,student_id):
    try:
        stu = Student.objects.get(pk=int(student_id))
        oops = False
    except:
        oops = True


    if request.method == "POST":
        print request.POST
        for ans in request.POST:
            post = request.POST
            if ans.startswith("praq") and len(post[ans]) > 0:
                pa,created = PracticalAnswer.objects.get_or_create(question_id=int(ans[4:]),student=stu)
                pa.answer = post[ans]
                pa.save()

        return redirect(request.path)


    pracs = PracticalExam.objects.all().order_by('position')

    select = SelectStudentForm(request,initial={'student':request.path})

    maxlen = 0
    table = {}
    table['body'] = []
    for prac in pracs:
        qset = prac.practicalquestion_set.all().order_by('position')
        if len(qset) > maxlen:
            maxlen = len(qset)
        row = []
        for q in qset:
            try:
                s = PracticalAnswer.objects.get(student=stu,question=q).answer
            except:
                s = ''
            row.append({'q':q,'score':s})
        table['body'].append(row)
    row = []
    for i in range(maxlen):
        row.append(i+1)
    #table['header'] = row
    print table
    print maxlen

    #return HttpResponse('ok',content_type='text/plain')
    missing = list_missing_corrections(45)

    return render_to_response('staff_score.html',{
        'oops':oops,
        'form':select,
        'table':table,
        'missing':missing
    })

""" list missing corrections """
def list_missing_corrections(num):
    return Student.objects.raw("SELECT * FROM (SELECT s.id, COUNT(s.id) AS count, s.user_id ,u.first_name,u.last_name FROM question_student s JOIN auth_user u ON u.id = s.user_id LEFT JOIN question_practicalanswer a ON s.id = a.student_id GROUP BY s.id ORDER by count ASC) t WHERE count < {0}".format(int(num)))

   
@staff_member_required
def results_theory(request,exam_id):

    studis = Student.objects.select_related().all()
    masterkey = Student.objects.get(user__id=303)
    print masterkey.user.username
    solution = ExamAnswers.objects.filter(user=303,question__exam=exam_id).order_by('question__position')
    print len(solution)
    slist = []
    sums = []
    for s in studis:
        zum = 0
        qlist = []
        i = 0
        print "studi"
        for q in solution:
            #print i,q.question.position
            assert q.question.position == i+1
            try:
                a = ExamAnswers.objects.get(user=s.user,question__exam=exam_id,question__position=i+1)
            except:    
                print i,'notfound'
                qlist.append(0)
                i += 1
                continue
             
            count = 0
            #print q, a
            if q.answer1==a.answer1:
                count +=1
            if q.answer2==a.answer2:
                count +=1
            if q.answer3==a.answer3:
                count +=1
            if q.answer4==a.answer4:
                count +=1
            
            qlist.append(count)
            zum += count
            i += 1
        slist.append({'s':s,'score':qlist,'sum':zum})
        sums.append(zum)

    return render_to_response('results.html',{'list':slist})


 
