from django.conf.urls.defaults import *
from ibo2013.views import *
from ibo2013.question import views as iboview
from django.views.generic.simple import redirect_to


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    ('^$',redirect_to,{'url':'/jury/1/'}),
    ('^accounts/profile/$',redirect_to,{'url':'/jury/1/'}),
    (r'^exam/(\d{1,9})/$',iboview.view_exam),
    (r'^jury/(?P<lang_id>\d{1,9})/$',iboview.jury_profile),
    (r'^jury/(?P<lang_id>\d{1,9})/overview/$',iboview.jury_overview),
    (r'^jury/(?P<lang_id>\d{1,9})/exam/(?P<exam_id>\d{1,9})/$',iboview.jury_examview),
    (r'^question/(\d{1,9})/$',iboview.view_question),
    (r'^question/(\d{1,9})/history/$',iboview.view_question_history),
    (r'^jury/(?P<lang_id>\d{1,9})/exam/(?P<exam_id>\d{1,9})/question/(?P<question_position>\d{1,2})/translate/$',iboview.jury_questionview),
    (r'^accounts/login/$', 'django.contrib.auth.views.login',{'template_name': 'auth.html'}),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout',{'next_page': '/accounts/login'}),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
