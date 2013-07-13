from django.conf.urls import patterns, include, url
# from django.conf.urls.defaults import *
from xuezhangshuo import settings
import django.views.static
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.auth.views import login, logout_then_login
admin.autodiscover()

urlpatterns = patterns('xuezhangshuo.views',
    # Example:
                         # (r'^rate/', include('rate.foo.urls')),

                      # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
                      # to INSTALLED_APPS to enable admin documentation:
                         # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

                      # Uncomment the next line to enable the admin:
                      (r'^admin/', include(admin.site.urls)),
                      #('^(\w\w\d\d\d)/(.*?)/$','classPage'),
                      ('^$','homePage'),
                      # (r'^static/(?P<path>.*)$',django.views.static.serve,{'document_root':settings.STATIC_PATH}),
                      # (r'^media/(?P<path>.*)$',django.views.static.serve,{'document_root':settings.STATIC_PATH}),
                      (r'^login/$',  login, {'template_name':'LoginPage.html'}),
                      (r'^logout/$', logout_then_login, {'login_url':'/login'}),
#{'template_name':'LoginPage.html', 'next_page':}),
                      (r'^(\w\w\d\d\d)/$','coursePage'),
                      (r'^vote/(\w\w\d\d\d)/(.*?)/$','votePage'),
                      # (r'^mylogin$','dev_login'),
                      (r'^profile/(.*?)/$','profilePage'),
                      (r'^api/vote/$','APIvote'),
                      (r'^api/makeComment/$','APImakeComment'),
                      (r'^api/getCourseTeacherScore/$','APIgetCourseTeacherScorePage'),
                      (r'^api/getCourseComment/$','APIgetCourseCommentPage'),
                      (r'^apidoc/$','APIdocPage'),
                      (r'^guestbook/$','guestbookPage'),
                      (r'^register/$','registerPage'),
                      #(r'^sutuo/$', 'sutuoPage'),
                      #(r'^tuosou/$', 'sutuoPage'),
)
