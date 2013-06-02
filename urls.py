from django.conf.urls.defaults import *
from ibo2013.views import *
from ibo2013.books import views
from ibo2013.question import views as iboview


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^ibo2013/', include('ibo2013.foo.urls')),
    ('^hello/$',hello),
    ('^$',current_datetime),
    (r'^time/plus/(\d{1,2})/$',hours_ahead),
    ('^meta/$',display_meta),
    (r'^exam/(\d{1,9})/$',iboview.view_exam),
    (r'^jury/(\d{1,9})/overview/$',iboview.jury_overview),
    (r'^jury/(\d{1,9})/exam/(\d{1,9})/$',iboview.jury_examview),
    (r'^exam/(\d{1,9})/translate/(\d{1,2})/$',iboview.translation_overview),
    (r'^question/(\d{1,9})/$',iboview.view_question),
    (r'^question/(\d{1,9})/history/$',iboview.view_question_history),
    (r'^jury/(\d{1,9})/exam/(\d{1,9})/question/(\d{1,2})/translate/$',iboview.jury_questionview),

    (r'^search-form/$', views.search_form),
    (r'^search/$', views.search),
    (r'^accounts/login/$', 'django.contrib.auth.views.login',{'template_name': 'auth.html'}),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
