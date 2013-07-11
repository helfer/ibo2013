from django.shortcuts import render_to_response, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect
from ibo2013.question.models import *
from django.db.models import Count
from django.db import connections
from django.template import RequestContext
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from ibo2013.question import qml
from django.db.models import Q
from xml.etree import ElementTree as et



@login_required
def question(request,language_id,exam_id,question_position):

    if int(exam_id) not in [1,2]:
        raise PermissionDenied() #TODO: just a hack to keep people out
    try:
        question_position = int(question_position)
        exam_id = int(exam_id)
        language = Language.objects.get(id=language_id)
        question = Question.objects.get(exam__id=exam_id,examquestion__position=question_position)
        vnode = question.versionnode_set.filter(language=language.id).order_by('-timestamp')[0]
    except: 
        raise Http404()

    xmlq = qml.QMLquestion(vnode.text)
    struct = xmlq.get_texts_nested(prep=True)

    return render_to_response('students_questionview.html',{'language':language,'question':question,'vnode':vnode,'struct':struct})
