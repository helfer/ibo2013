from django.http import HttpResponse, HttpResponseBadRequest
import traceback
from django.utils import simplejson as json
from django.views.generic import UpdateView
from ibo2013.question.models import *

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
