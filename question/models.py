from django.db import models
from django.contrib.auth.models import User
from ibo2013.question import simplediff



def dictify(obj_list,key):
    ret = {}
    for obj in obj_list:
        ret[getattr(obj,key)] = obj
    return ret

class Language(models.Model):
    name = models.CharField(max_length=100,unique=True)
    coordinators = models.ManyToManyField(User,related_name='coordinator_set')
    editors = models.ManyToManyField(User,related_name='editor_set')

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
    checkout = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)
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
        print categories

        cid = -1
        objs = []
        for q in self.question_status:
            if q['primary'].category_id != cid:
                cid = q['primary'].category_id
                print "cid " + str(cid)
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

            SELECT eq.*, vn.text, vn.version, vn.id as vid
            FROM question_examquestion eq
            LEFT OUTER JOIN (
                SELECT *
                FROM question_versionnode
                WHERE language_id ='%s'
            ) AS vn ON eq.question_id = vn.question_id
            WHERE eq.exam_id='%s'
            ORDER BY position, version DESC
            ) AS t1
            GROUP BY position
            ORDER BY category_id,position"""
        q1params = [1,self.id] #todo: english = 1 is hardcoded as primary language

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

        questions = []
        for i in range(len(pv)):
            questions.append({"primary":pv[i],"target":tv[i]})
            if tv[i].vid is None:
                questions[i]["status"] = "empt"
            elif tv[i].origin_id != pv[i].vid:
                questions[i]["status"] = "updt"
            elif tv[i].flag:
                questions[i]["status"] = "flag"
            elif tv[i].checkout:
                questions[i]["status"] = "done"
            else:
                questions[i]["status"] = "need"
 
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


