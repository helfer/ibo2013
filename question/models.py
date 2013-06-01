from django.db import models
from django.contrib.auth.models import User
from ibo2013 import simplediff


class Language(models.Model):
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return u'%s' % (self.name)


class Question(models.Model):
    name = models.CharField(max_length=100)
    primary_language = models.ForeignKey(Language)
    def __unicode__(self):
        return u'%s' % (self.name)

    def __str__(self):
        return "question:"+self.name


class VersionNode(models.Model):
    text = models.TextField()
    question = models.ForeignKey(Question)
    version = models.IntegerField()
    language = models.ForeignKey(Language)
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

    def __unicode__(self):
        return u'Exam: %s' % (self.name)




    #reassigns positions to exam questions such that each position is unique
    def order_questions(self):
      qr = ExamQuestion.objects.filter(exam=self).order_by('position')
      for i in range(len(qr)):
        qr[i].position = i+1
        qr[i].save()


    def check_permission(self,user,lang):
        if user.is_superuser:
            return True
        else:
            return self.exampermission_set.filter(user=user,language=lang).exists()

    def add_permission(self,user,lang):
        self.exampermission_set.create(language=lang,user=user)
        self.save()

class ExamPermission(models.Model):
    exam = models.ForeignKey(Exam)
    language = models.ForeignKey(Language)
    user = models.ForeignKey(User)


class ExamQuestion(models.Model):
    exam = models.ForeignKey(Exam)
    question = models.ForeignKey(Question)
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

   
 


