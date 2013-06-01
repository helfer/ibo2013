from django.http import Http404, HttpResponse
import datetime

def hello(request):
	return HttpResponse("Hello wolrd")

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def hours_ahead(request,offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    later = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>Soon it will be %s.</body></html>" % later
    return HttpResponse(html)

def display_meta(request):
    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))

