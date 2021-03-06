from django import forms
from django.forms import ModelForm
from ibo2013.question.models import *
from ibo2013.question.widgets import QMLTableWidget,QMLRowWidget
from django.forms.util import ValidationError
#from ckeditor.widgets import CKEditorWidget
import json

class EditQuestionForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'id':'area51','rows':40,'cols':120}))
    comment = forms.CharField(widget=forms.Textarea,required=False)
    flag = forms.BooleanField(required=False)
    checkout = forms.BooleanField(required=False)
    commit = forms.BooleanField(required=False)

class JuryQuestionForm(forms.Form):
    text = forms.CharField(required=False,widget=forms.Textarea(attrs={'id':'area51','rows':40,'cols':120}))
    comment = forms.CharField(widget=forms.Textarea,required=False)
    flag = forms.BooleanField(required=False)
    orig = forms.IntegerField(widget=forms.HiddenInput)
    rating = forms.IntegerField(required=False)
    checkout = forms.BooleanField(required=False)

#same as above, but readonly, can never be submitted
class ViewQuestionForm(EditQuestionForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'readonly':'readonly'}))
    comment = forms.CharField(widget=forms.Textarea(attrs={'readonly':'readonly'}),required=False)
        
    def is_valid():
        return False

#adds a new question to an exam
class AddQuestionForm(ModelForm):
    position = forms.CharField(initial=999,label="Position")
    points = forms.CharField(initial=1,label="Points")
    category = forms.ModelChoiceField(queryset=QuestionCategory.objects.all(),empty_label=None)

    class Meta:
        model = Question
        fields = ['name']

class AddCategoryForm(ModelForm):
    title = forms.CharField(label="Full English name")    

    class Meta:
        model = QuestionCategory

class EditCategoryForm(ModelForm):

    class Meta:
        model = QuestionCategory

class TranslateCategoryForm(ModelForm):
    
    class Meta:
        model = CategoryTranslation
        fields = ['text']

class ChangePointsForm(ModelForm):
    class Meta:
        mode = Question
        fields = ['points']


#swap the position of two questions
class SwapQuestionForm(forms.Form):
    pass
    #move up button (has no effect if first question)
    #move down button (has no effect if last question)

class AddLanguageForm(forms.Form):
    name = forms.CharField(label="Language name:")

class EditLanguageForm(forms.Form):
    dlg = forms.ModelChoiceField(queryset=Delegation.objects.all(),label="Give access to")
    


class PickLanguageForm(forms.Form):

    def __init__(self,user,lang_id,request,languages=None,realpath=None,pos=2,*args,**kwargs):
        super(PickLanguageForm,self).__init__(*args,**kwargs)
        self.lang_id = lang_id
        self.user_id = user.id
        if realpath is None:
            realpath = request.path
        if languages is None:
            languages = Language.objects.filter(hidden=False).order_by('-official','name')
        choices = []
        for l in languages:
            ps = realpath.split("/")
            ps[pos] = str(l.id)
            path = "/".join(ps)
            choices.append((path,l.name))

        self.fields['language'] = forms.ChoiceField(
            choices=choices,
            widget = forms.Select(attrs={'onchange':'window.location = this.value;'}),
            )
    


class QMLform(forms.Form):


    def __init__(self,*args,**kwargs):
        qml = kwargs.pop("qml")
        super(QMLform,self).__init__(*args,**kwargs)

        for i,el in enumerate(qml.get_form_elements()):
            self.fields[el[0]] = el[1]

class QMLTableField(forms.MultiValueField):
    #widget = forms.widgets.Textarea

    def __init__(self,rows,*args,**kwargs):
        self.rows = rows
        self.rown = len(rows)
        self.coln = len(rows[0])
        print "rowcol",self.rown*self.coln
        kwargs["widget"] = QMLTableWidget(rows)
        kwargs["fields"] = [QMLRowField(row,label=None) for row in rows]
        kwargs["required"] = False
        super(QMLTableField,self).__init__(*args,**kwargs)

        print "my fields:", self.fields

    #XXX just for testing, don't actually use those separators
    def compress(self,data_list):
        
        print data_list
        if not data_list:
            print "compress nothing?"
            return ''
        out = []
        rown = len(self.rows)
        coln = len(self.rows[0])
        print rown,coln,len(data_list)
        #assert rown*coln == len(data_list)
        #newrows = chunky(data_list,coln)
        return json.dumps(data_list)

class QMLRowField(forms.MultiValueField):

    def __init__(self,row,*args,**kwargs):
        self.row = row
        kwargs["widget"] = QMLRowWidget(row)
        kwargs["fields"] = [forms.CharField(label=None) for i in xrange(0,len(self.row))]
        super(QMLRowField,self).__init__(*args,**kwargs)

    def compress(self,data_list):
        
        if not data_list:
            return ''

        return json.dumps(data_list)

class AddExamquestionForm(forms.Form):
    question = forms.ModelChoiceField(queryset=Question.objects.all(),empty_label=None)
    position = forms.IntegerField()

class UpdateCategoryForm(forms.ModelForm):
    class Meta:
        model = ExamQuestion
        fields = ['points','category']

class UploadFigureForm(forms.Form):
    name = forms.CharField(max_length=100,required=False)
    description = forms.CharField(max_length=100,required=False)
    imgfile = forms.FileField()


class FigureChoiceForm(forms.Form):
    figure = forms.ModelChoiceField(queryset=Figure.objects.all(),empty_label=None)


class UploadPracticalForm(forms.Form):
    name = forms.CharField(max_length=100,required=False)
    pfile = forms.FileField()
   
    #def clean_pfile(self):
    #    value = self.cleaned_data["pfile"]
    #    if not value.name.endswith('.pdf'):
    #        raise ValidationError("Please upload only files in pdf format")

class AssignPracticalForm(forms.Form):

    def __init__(self,*args,**kwargs):
        students = kwargs.pop("students")
        practicals = kwargs.pop("practicals")
        super(AssignPracticalForm,self).__init__(*args,**kwargs)
        staffd = Delegation.objects.get(name="Exam_Staff")
        for s in students:
            for p in practicals:
                self.fields["{0}__{1}".format(s.id,p.id)] = forms.ModelChoiceField(
                    queryset=PracticalExamFile.objects.filter(delegation=s.delegation)|PracticalExamFile.objects.filter(delegation=staffd),
                    empty_label=None,
                    label="{0} {1} ({2})".format(s.user.first_name.encode('utf-8'),s.user.last_name.encode('utf-8'),p.name))

            
class StaffVoteForm(forms.ModelForm):
     class Meta:
        model = VotingRound


class CatTransForm(forms.Form):

    def __init__(self,*args,**kwargs):
        super(CatTransForm,self).__init__(*args,**kwargs)
        cats = QuestionCategory.objects.all().order_by('name')
        for c in cats:
            self.fields["f"+str(c.id)] = forms.CharField(max_length=100,required=False,label=c.name)



class SelectStudentForm(forms.Form):
    
    def __init__(self,request,*args,**kwargs):
        super(SelectStudentForm,self).__init__(*args,**kwargs)
        students = Student.objects.select_related().all().order_by('user__first_name','user__last_name')
        choices = []
        for s in students:
            pth = request.path.split('/')
            pth[-2] = str(s.id)
            choices.append(("/".join(pth),str(s)))
            self.fields['student'] = forms.ChoiceField(
            choices=choices,
            widget = forms.Select(attrs={'onchange':'window.location = this.value;'}),
            )

class DelegationExamLanguagesForm(forms.ModelForm):
     class Meta:
        model = Delegation
        fields = ['exam_languages']
