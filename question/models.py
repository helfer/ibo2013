import os
from django.db import models
from django.contrib.auth.models import User,Group
from ibo2013.question import simplediff
from xml.etree import ElementTree as et


PRIMARY_LANG_ID=1

def dictify(obj_list,key):
    ret = {}
    for obj in obj_list:
        ret[getattr(obj,key)] = obj
    return ret

class Language(models.Model):
    name = models.CharField(max_length=100,unique=True)
    coordinators = models.ManyToManyField(User,related_name='coordinator_set')
    editors = models.ManyToManyField(User,related_name='editor_set')
    official = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % (self.name)

    def check_permission(self,user):
        if user.is_superuser:
            return True
        else:
            return self.editors.filter(user=user).exists() or self.coordinators.filter(user=user).exists()

class Question(models.Model):
    name = models.CharField(max_length=100)
    primary_language = models.ForeignKey(Language)

    def __unicode__(self):
        return u'%s' % (self.name)

    def __str__(self):
        return "question:"+self.name


    def get_newest_version():
        return self.versionnode_set.order_by('-timestamp')[0]

class QuestionCategory(models.Model):
    name = models.CharField(max_length=100)
    position = models.IntegerField() #position in exam

    def __unicode__(self,empty_label=None):
        return self.name

class CategoryTranslation(models.Model):
    category = models.ForeignKey(QuestionCategory)
    language = models.ForeignKey(Language)
    text = models.CharField(max_length=100)



class VersionNode(models.Model):
    text = models.TextField()
    comment = models.TextField()
    question = models.ForeignKey(Question)
    version = models.IntegerField()
    language = models.ForeignKey(Language)
    flag = models.BooleanField()
    rating = models.IntegerField(null=True)
    checkout = models.BooleanField()
    committed = models.BooleanField()
    timestamp = models.DateTimeField(auto_now=True)
    #committed = models.BooleanField(default=False)
    
    def __unicode__(self):
        return u'VersionNode: %s (%s)[v%s]' % (self.question.name,self.language,self.version)

    def compare_with(self,vn2):
        return simplediff.html_diff(self.text,vn2.text)

class Translation(models.Model):
    """stores relationships between primary and secondary language"""
    language = models.ForeignKey(Language)
    origin = models.ForeignKey(VersionNode,related_name='translation_origin')
    target = models.ForeignKey(VersionNode,unique=True,related_name='translation_target')        
    
    def __unicode__(self):
        return u'Translation Object vnode %s to vnode %s lang %s' % (language,origin,target)

class Exam(models.Model):
    name = models.CharField(max_length=100)
    languages = models.ManyToManyField(Language)
    questions = models.ManyToManyField(Question,blank=True,null=True,through='ExamQuestion')
    staff_only = models.BooleanField(default=False)


    def __init__(self,*args,**kwargs):
        self.question_status = None
        super(Exam,self).__init__(*args,**kwargs)

    def __unicode__(self):
        return u'Exam: %s' % (self.name)




    #reassigns positions to exam questions such that each position is unique
    def order_questions(self):
        qr = ExamQuestion.objects.filter(exam=self).order_by('position')
        for i in range(len(qr)):
            qr[i].position = i+1
            qr[i].save()


      #qr = ExamQuestion.objects.filter(exam=self).order_by('category_id','position')
      #ccid = -1
      #pos = 0
      #for q in qr:
      #  if q.category_id != ccid:
      #      pos = 1
      #      ccid = q.category_id
      #  qr[i].position = pos
      #  qr[i].save()
      #  pos += 1


    def check_permission(self,user,lang):
        if user.is_superuser:
            return True
        else:
            return self.exampermission_set.filter(user=user,language=lang).exists()

    def add_permission(self,user,lang):
        self.exampermission_set.create(language=lang,user=user)
        self.save()


    def get_categorized_status(self,lang_id):
        if self.question_status is None:
            self.load_question_status(lang_id)

        current_cat = 0
        categories = CategoryTranslation.objects.filter(language=1).order_by('category')
        categories = dictify(categories,'category_id')

        cid = -1
        objs = []
        for q in self.question_status:
            if q['primary'].category_id != cid:
                cid = q['primary'].category_id
                objs.append({'cat':categories[cid],'questions':[]})

            objs[-1]['questions'].append(q)

        return objs

    #strictly speaking this should be in views.py, but I find it more convenient to access here
    def load_question_status(self,lang_id):
        
        if self.question_status is not None:
            return

        #questions = self.examquestion_set.order_by('position')

        #selects all the most recent english versions of questions from this exam
        query = """SELECT * FROM (

            SELECT eq.*, vn.text, vn.version, vn.id as vid, vn.flag, vn.checkout
            FROM question_examquestion eq
            LEFT OUTER JOIN (
                SELECT *
                FROM question_versionnode
                WHERE language_id ='%s' AND committed = 1
            ) AS vn ON eq.question_id = vn.question_id
            WHERE eq.exam_id='%s'
            ORDER BY position, version DESC
            ) AS t1
            GROUP BY position
            ORDER BY category_id,position"""
        q1params = [PRIMARY_LANG_ID,self.id] #todo: english = 1 is hardcoded as primary language

        primary_versions = ExamQuestion.objects.raw(query,q1params)

        #selects the most recent target translatsion versions of questions in exam
        query2 = """SELECT t1.*,tr.origin_id,tr.target_id FROM (
            SELECT eq.*, vn.text, vn.version, vn.flag, vn.checkout, vn.id as vid 
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
            GROUP BY position
            ORDER BY category_id,position"""
        q2params = [lang_id,self.id]

        target_versions = ExamQuestion.objects.raw(query2,q2params)

        pv = list(primary_versions)
        tv = list(target_versions)
        assert len(pv) == len(tv) #if not, you screwed up the queries

        #import at file start fails due to some cyclic dependencies
        #from ibo2013.question import qml
        
        questions = []
        for i in range(len(pv)):
            try:
                if tv[i].text is None:
                    preview = et.fromstring(pv[i].text.encode('utf-8')).find('./text').text
                else:
                    preview = et.fromstring(tv[i].text.encode('utf-8')).find('./text').text
                if len(preview) > 130:
                    preview = preview[:127] + "..."
            except:
                    preview = pv[i].text #fallback if not XML or no text element
            questions.append({"primary":pv[i],"target":tv[i],"preview":preview})
            if tv[i].vid is None:
                questions[i]["status"] = "empt"
            elif tv[i].origin_id != pv[i].vid:
                questions[i]["status"] = "updt"
            elif tv[i].checkout:
                questions[i]["status"] = "done"
            else:
                questions[i]["status"] = "need"
            #flag is independent of others.
            if tv[i].flag:
                questions[i]["status"] += " flag"
            
            #primary lang is special case
            if lang_id == PRIMARY_LANG_ID:
                if pv[i].checkout:
                    questions[i]["status"] = "done"
                else:
                    questions[i]["status"] = "need"
                if pv[i].flag:
                    questions[i]["status"] += " flag"
            
 
        self.question_status = questions



class ExamPermission(models.Model):
    exam = models.ForeignKey(Exam)
    language = models.ForeignKey(Language)
    user = models.ForeignKey(User)


class ExamQuestion(models.Model):
    exam = models.ForeignKey(Exam)
    question = models.ForeignKey(Question)
    category = models.ForeignKey(QuestionCategory)
    position = models.IntegerField()
    points = models.DecimalField(max_digits=5,decimal_places=2)


    def __unicode__(self):
        return u'ExamQuestion: %s' % self.position

    # swaps the positions of two questions in the exam
    def swap_position(self,q2):
      tmp = self.position
      self.position = q2.position
      q2.position = tmp
      self.save()
      q2.save()

class Figure(models.Model):
    name = models.CharField(unique=True,max_length=100)   
    description = models.TextField()
    svg = models.TextField() 
    var = models.TextField()

    def __unicode__(self):
        return self.name

class Delegation(models.Model):
    name = models.CharField(unique=True,max_length=100)
    group = models.ForeignKey(Group)
    members = models.ManyToManyField(User)

    def __unicode__(self):
        return self.name

class PracticalExam(models.Model):
    name = models.CharField(unique=True,max_length=100)
    filename = models.CharField(unique=True,max_length=100)
    position = models.IntegerField()
    en_official = models.CharField(max_length=100)
    ru_official = models.CharField(max_length=100)

class PracticalExamFile(models.Model):
    name = models.CharField(max_length=100)
    filename = models.CharField(unique=True,max_length=200) #this is the actual filenmame for serving
    delegation = models.ForeignKey(Delegation)
    timestamp = models.DateTimeField(auto_now=True)
    content_type = models.CharField(max_length=100,null=True)
    owner = models.ForeignKey(User)


    def __unicode__(self):
        return self.name

    def handle_uploaded_file(self,f):
        self.content_type = f.content_type
        with open('/var/www/django/ibo2013/uploaded_files/'+self.filename, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

    def delete_file(self):
        os.remove('/var/www/django/ibo2013/uploaded_files/'+self.filename)


class Student(models.Model):
    user = models.ForeignKey(User)
    examfile = models.ManyToManyField(PracticalExamFile,through='PracticalAssignment')
    delegation = models.ForeignKey(Delegation)

    def __unicode__(self):
        return self.user.first_name + ' ' + self.user.last_name

class PracticalAssignment(models.Model):
    student = models.ForeignKey(Student)
    practical_exam_file = models.ForeignKey(PracticalExamFile,null=True)
    practical_exam = models.ForeignKey(PracticalExam)
    finalized = models.BooleanField(default=False)
    printed = models.BooleanField(default=False)   
 
    def __unicode__(self):
        return "{0}-{1}-{2}".format(self.student_id,self.practical_exam_id,self.practical_exam_file_id)



class VotingRound(models.Model):
    text = models.CharField(max_length=500)
    active = models.BooleanField()
    closed = models.BooleanField()

class Vote(models.Model):
    VOTECHOICE = (
        ('y', 'yes'),
        ('n', 'no'),
        ('a', 'abstain'),
    )
    answer = models.CharField(max_length=20)
    vround = models.ForeignKey(VotingRound)
    delegation = models.ForeignKey(Delegation)

    def __unicode__(self):
        return self.delegation.name + str(self.vround.id) + self.answer

# yeah, this is dumb
class ExamAnswers(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(ExamQuestion)
    answer1 = models.NullBooleanField()
    answer2 = models.NullBooleanField() 
    answer3 = models.NullBooleanField() 
    answer4 = models.NullBooleanField() 
    timestamp = models.DateTimeField(auto_now=True)


class ExamFlags(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(ExamQuestion)

class SimpleLog(models.Model):
    user = models.ForeignKey(User,null=True)
    path = models.CharField(max_length=200)
    ip = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now=True,null=True)
    info = models.CharField(max_length=200)

