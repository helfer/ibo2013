from django.core.servers.basehttp import FileWrapper
from django.http import Http404,HttpResponse
import os
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import permission_required,login_required
from django.contrib.admin.views.decorators import staff_member_required
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

def read_jury_page(user):
    if user:
        try:
            return user.is_staff or user.is_superuser or user.groups.get(name='Jury')
        except:
            return False

#flie download view for everyone
@login_required
@permission_required('question.is_jury')
def secure_download(request,fname=None):
    if fname is None:
        raise Http404()
    #try:
    filename = '/var/www/django/ibo2013/uploaded_files/'+fname                                
    wrapper = FileWrapper(file(filename))
    response = HttpResponse(wrapper,content_type="application/pdf")
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'attachment; filename={0}'.format(fname)
    return response
    #except:
    #    raise Http404()
    #find out if file exists on disk
    #find out if user is supposed to be able to access it.
    #assume yes if jury
    #return the file

#download view for staff members
@staff_member_required
def staff_download(request,filename):
    pass


def handle_uploaded_file(f,filename):
    with open('/var/www/django/ibo2013/files/'+filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
