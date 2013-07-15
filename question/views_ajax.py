from django.http import HttpResponse, HttpResponseBadRequest
import traceback
from django.utils import simplejson as json
from django.views.generic import UpdateView
from ibo2013.question.models import *
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def ajax_update(request):

    if request.is_ajax():
        print "AJAX"
        #print request.POST
        try:
            vn = VersionNode.objects.get(id=int(request.POST['vnode']))
            print vn.id
            if vn.committed:
                print "can't commit"
                return HttpResponseBadRequest(json.dumps("cannot update committed vnode"),mimetype="application/json")
            
            vn.text = request.POST['text']
            vn.save()
            print "saved"
            return HttpResponse(json.dumps("success, vnode saved"),mimetype="application/json")
        except:
            print traceback.format_exc()
            return HttpResponseBadRequest(json.dumps("server error"),mimetype="application/json")


    else:
        print "ERROR"
        return HttpResponseBadRequest(json.dumps("not ajax"),mimetype="application/json");


def ajax_flag(request):
    if request.is_ajax():
        try:
            eq = ExamQuestion.objects.get(id=request.POST['qid'])
            flg,created = ExamFlags.objects.get_or_create(user=request.user,question=eq)
            if request.POST['flag'] == "true":
                pass
            else:
                flg.delete()
            return HttpResponse(json.dumps("success, flag saved"),mimetype="application/json")
        except:
            return HttpResponseBadRequest("not ajax")


    else:
        return HttpResponseBadRequest("not ajax")


def ajax_answer(request):
    if request.is_ajax():
        print request.POST
        try:
            eq = ExamQuestion.objects.get(id=request.POST['qid'])
            print eq
            answer,created = ExamAnswers.objects.get_or_create(user=request.user,question=eq)
            print answer
            if int(request.POST['ans']) == 3:
                answer.answer1 = request.POST['choice'] == "true"
            elif int(request.POST['ans']) == 4:
                answer.answer2 = request.POST['choice'] == "true"
            elif int(request.POST['ans']) == 5:
                answer.answer3 = request.POST['choice'] == "true"
            elif int(request.POST['ans']) == 6:
                answer.answer4 = request.POST['choice'] == "true"
            else:
                return HttpResponseBadRequest("unknown question number")
            answer.save()
            return HttpResponse(json.dumps("success, flag saved"),mimetype="application/json")
        except Exception as e:
            print e
            return HttpResponseBadRequest("not ajax")


    else:
        return HttpResponseBadRequest("not ajax")
