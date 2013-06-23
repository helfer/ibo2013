from django import forms
from django.forms import ModelForm
from ibo2013.question.models import *

class EditQuestionForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    comment = forms.CharField(widget=forms.Textarea,required=False)
    flag = forms.BooleanField(required=False)
    checkout = forms.BooleanField(required=False)

    def __init__(self,permissions=None,*args,**kwargs):
        super(EditQuestionForm,self).__init__(*args,**kwargs)
        if permissions is None or not ('admin' in permissions or 'edit' in permissions):
            self.fields['text'] = forms.CharField(widget=forms.Textarea(attrs={'readonly':'readonly'}))
            self.fields['comment'] = forms.CharField(widget=forms.Textarea(attrs={'readonly':'readonly'}),required=False)

#adds a new question to an exam
class AddQuestionForm(ModelForm):
    position = forms.CharField(label="Position")
    points = forms.CharField(label="Points")

    class Meta:
        model = Question


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
    
    #
