from ibo2013.question.models import SimpleLog

class LoggingMiddleware(object):





    def process_request(self,request):
        u = request.user
        if u.is_anonymous():
            u = None
        l = SimpleLog(user=u, path=request.path,ip=self.get_client_ip(request))
        l.save()

    def get_client_ip(self,request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
