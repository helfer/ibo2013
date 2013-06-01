from django import forms
from django.forms import ModelForm
from ibo2013.question.models import *

class EditQuestionForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)


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
