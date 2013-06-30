import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'ibo2013.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

path = '/var/www/django/ibo2013/'
path2 = '/var/www/django/'
path3 = '/var/www/django/debug_toolbar'

if path not in sys.path:
    sys.path.append(path)
    sys.path.append(path2)
    sys.path.append(path3)


from ibo2013 import monitor

monitor.start(interval=1.0)
