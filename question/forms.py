from django import forms
from django.forms import ModelForm
from ibo2013.question.models import *
from ibo2013.question.widgets import QMLTableWidget

class EditQuestionForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'id':'area51','rows':40,'cols':120}))
    comment = forms.CharField(widget=forms.Textarea,required=False)
    flag = forms.BooleanField(required=False)
    checkout = forms.BooleanField(required=False)

    #def __init__(self,permissions=None,*args,**kwargs):
    #    super(EditQuestionForm,self).__init__(*args,**kwargs)
        #if permissions is None or not ('admin' in permissions or 'edit' in permissions):
        #    self.fields['text'] = forms.CharField(widget=forms.Textarea(attrs={'readonly':'readonly'}))
        #    self.fields['comment'] = forms.CharField(widget=forms.Textarea(attrs={'readonly':'readonly'}),required=False)

#same as above, but readonly, can never be submitted
class ViewQuestionForm(EditQuestionForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'readonly':'readonly'}))
    comment = forms.CharField(widget=forms.Textarea(attrs={'readonly':'readonly'}),required=False)
        
    def is_valid():
        return False

#adds a new question to an exam
class AddQuestionForm(ModelForm):
    position = forms.CharField(label="Position")
    points = forms.CharField(label="Points")

    class Meta:
        model = Question
        fields = ['name']

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

class EditLanguageForm(ModelForm):
    class Meta:
        model = Language
        fields = ['coordinators','editors']


class PickLanguageForm(forms.Form):

    def __init__(self,user,lang_id,request,*args,**kwargs):
        super(PickLanguageForm,self).__init__(*args,**kwargs)
        self.lang_id = lang_id
        self.user_id = user.id
        languages = Language.objects.all().order_by('name')
        choices = []
        for l in languages:
            ps = request.path.split("/")
            ps[2] = str(l.id)
            path = "/".join(ps)
            choices.append((path,l.name))

        self.fields['language'] = forms.ChoiceField(choices=choices)
    


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
        kwargs["widget"] = QMLTableWidget(rows)
        super(QMLTableField,self).__init__(*args,**kwargs)

    #XXX just for testing, don't actually use those separators
    def compress(self,data_list):
        if not data_list:
            print data_list
            print "compress nothing?"
            return ''
        out = []
        rown = len(self.rows)
        coln = len(self.rows[0])
        print rown,coln,len(data_list)
        assert rown*coln == len(data_list)
        newrows = chunky(data_list,coln)
        for row in newrows:
            out.append("&*(".join(row))

        return "#$%".join(out)

    def chunky(lst,n):
        for i in xrange(0,len(lst),n):
            yield lst[i:i+n]

