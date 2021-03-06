from django.conf.urls.defaults import *
from ibo2013.question import views_jury as juryview
from ibo2013.question import views_students as studentview
from ibo2013.question import views_staff as staffview
from ibo2013.question import views_common
from ibo2013.question import views_ajax as ajaxview
from django.views.generic.simple import redirect_to


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    ('^$',redirect_to,{'url':'/accounts/login/'}),
    
    ('^test/$',redirect_to,{'url':'/theory/'}),
    
    ('^theory/$',studentview.theory),

    (r'^jury/(?P<lang_id>\d{1,9})/$',juryview.profile),
    (r'^jury/(?P<lang_id>\d{1,9})/practical$',juryview.practical),
    (r'^jury/(?P<lang_id>\d{1,9})/students/$',juryview.students),
    (r'^jury/(?P<lang_id>\d{1,9})/theory/$',juryview.theoryresults),
    (r'^jury/(?P<lang_id>\d{1,9})/overview/$',juryview.overview),
    #(r'^jury/(?P<lang_id>\d{1,9})/practical/$',juryview.practical),
    (r'^jury/(?P<lang_id>\d{1,9})/practical/$',juryview.results),
    (r'^jury/files/(?P<fname>[^/]+)/$',views_common.secure_download),
    (r'^jury/(?P<lang_id>\d{1,9})/exam/(?P<exam_id>\d{1,9})/$',juryview.examview),
    (r'^jury/(?P<lang_id>\d{1,9})/vote/$',juryview.vote),
    (r'^jury/(?P<lang_id>\d{1,9})/exam/(?P<exam_id>\d{1,9})/question/(?P<question_position>\d{1,9})/translate/$',juryview.xmlquestionview),
    (r'^jury/(?P<lang_id>\d{1,9})/exam/(?P<exam_id>\d{1,9})/question/(?P<question_position>\d{1,9})/translate/(?P<from_lang_id>\d{1,9})/$',juryview.xmlquestionview),
    (r'^jury/(?P<lang_id>\d{1,9})/results/$',juryview.results),

    (r'^students/(\d{1,9})/question/(\d{1,9})/(\d{1,9})/$',studentview.question),
    (r'^students/(\d{1,9})/overview/(\d{1,9})/$',studentview.examview),
    
    (r'^students/results/$',studentview.resultview),
    (r'^students/results/theory/$',studentview.theoryresults),
    (r'^students/results/practical/$',studentview.practicalresults),

    (r'^ajax/$',ajaxview.ajax_update),
    (r'^ajax/flag/$',ajaxview.ajax_flag),
    (r'^ajax/answer/$',ajaxview.ajax_answer),

    (r'^staff/discussion/(\d{1,9})/(\d{1,9})/$',staffview.discussion),
    (r'^staff/categories/(\d{1,9})/$',staffview.translate_categories),
    (r'^staff/images/$',staffview.upload_figure),
    (r'^staff/categories/$',staffview.view_categories),
    (r'^staff/images/(?P<fname>[^/]+)/$',staffview.view_image),
    (r'^staff/images/(?P<fname>[^/]+)/(?P<qid>\d{1,9})/$',staffview.view_image),
    (r'^staff/images/(?P<fname>[^/]+)/(?P<qid>\d{1,9})/(?P<lang_id>\d{1,9})/$',staffview.view_image),
    (r'^staff/images/(?P<fname>[^/]+)/(?P<qid>\d{1,9})/(?P<lang_id>\d{1,9})/(?P<version>\d{1,9})/$',staffview.view_image),
    (r'^staff/question/(\d{1,9})/$',staffview.view_question,{"mode":"xml"}),
    (r'^staff/question/(\d{1,9})/history/$',staffview.view_question_history),
    (r'^staff/getpdf/(\d{1,9})/(\d{1,9})/(\d{1,9})/$',staffview.get_pdf),
    (r'^staff/getpdf/(\d{1,9})/(\d{1,9})/$',staffview.get_pdf),
    (r'^staff/print_exam/(\d{1,9})/(\d{1,9})/$',staffview.print_exam),
    (r'^staff/print_exam/(\d{1,9})/$',staffview.print_exam),
    (r'^staff/exam/(\d{1,9})/$',staffview.view_exam),
    (r'^staff/practical/$',staffview.practical),
    (r'^staff/vote/$',staffview.vote),
    (r'^staff/score/(\d{1,9})/$',staffview.score_practical),
    (r'^staff/results/(\d{1,9})/$',staffview.results_theory),
    (r'^jury/filelist/$',juryview.filelist),
    
    
    (r'^accounts/login/$', 'django.contrib.auth.views.login',{'template_name': 'auth.html'}),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout',{'next_page': '/accounts/login'}),
    ('^accounts/profile/$',views_common.redirect_to_home),
    
    

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
