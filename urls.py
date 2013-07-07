from django.conf.urls.defaults import *
from ibo2013.question import views_jury as juryview
from ibo2013.question import views_staff as staffview
from django.views.generic.simple import redirect_to


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    ('^$',redirect_to,{'url':'/jury/1/'}),
    ('^accounts/profile/$',redirect_to,{'url':'/jury/1/'}),
    (r'^staff/exam/(\d{1,9})/$',staffview.view_exam),
    (r'^jury/(?P<lang_id>\d{1,9})/$',juryview.profile),
    (r'^jury/(?P<lang_id>\d{1,9})/students/$',juryview.students),
    (r'^jury/(?P<lang_id>\d{1,9})/overview/$',juryview.overview),
    (r'^jury/(?P<lang_id>\d{1,9})/exam/(?P<exam_id>\d{1,9})/$',juryview.examview),
    (r'^staff/question/(\d{1,9})/$',staffview.view_question),
    (r'^staff/categories/(\d{1,9})/$',staffview.translate_categories),
    (r'^staff/figures/$',staffview.upload_figure),
    (r'^staff/categories/$',staffview.view_categories),
    (r'^staff/images/(.+)/$',staffview.view_image),
    (r'^staff/question/(\d{1,9})/xml/$',staffview.view_question,{"mode":"xml"}),
    (r'^staff/question/(\d{1,9})/history/$',staffview.view_question_history),
    (r'^jury/(?P<lang_id>\d{1,9})/exam/(?P<exam_id>\d{1,9})/question/(?P<question_position>\d{1,2})/translate/$',juryview.questionview),
    (r'^accounts/login/$', 'django.contrib.auth.views.login',{'template_name': 'auth.html'}),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout',{'next_page': '/accounts/login'}),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
