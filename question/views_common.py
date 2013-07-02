from django.shortcuts import render_to_response
from ibo2013.question.models import *
from ibo2013.question.forms import *
from django.template import RequestContext


def render_with_context(request,*args,**kwargs):
    lang_id = args[1]["lang_id"]
    picker = PickLanguageForm(request.user,lang_id,request,initial={'language':request.path})
    kwargs['context_instance'] = RequestContext(request)
    args[1]["lang_picker"] = picker
    return render_to_response(*args,**kwargs)


#decorator that checks which permissions a user has.
def permission_check(f):
    def secure_f(*args,**kwargs):
        request = args[0]
        lang_id = kwargs['lang_id']
        permissions = ['read']

        if request.user.is_superuser:
            permissions = ['read','write','admin']
        else:

            if  Language.objects.get(id=lang_id).editors.filter(id=request.user.id).exists():
                permissions.append('write')
            if  Language.objects.get(id=lang_id).coordinators.filter(id=request.user.id).exists():
                permissions.append('admin')

        print args[0].user,kwargs,permissions

        res = f(*args,permissions=permissions,**kwargs)

        return res

    return secure_f

