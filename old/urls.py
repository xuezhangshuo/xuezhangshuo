from django.conf.urls.defaults import *
from XueZhangShuo import settings
import django.views.static
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('XueZhangShuo.views',
    # Example:
                         # (r'^rate/', include('rate.foo.urls')),

                      # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
                      # to INSTALLED_APPS to enable admin documentation:
                         # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

                      # Uncomment the next line to enable the admin:
                         (r'^admin/', include(admin.site.urls)),
                      #('^hello/$','hello'),
                      #('^(\w\w\d\d\d)/(.*?)/$','classPage'),
                      ('^$','homePage'),
                      (r'^static/(?P<path>.*)$',django.views.static.serve,{'document_root':settings.STATIC_PATH}),
                      (r'^media/(?P<path>.*)$',django.views.static.serve,{'document_root':settings.STATIC_PATH}),
                      (r'^login/$','loginPage'),
                      (r'^(\w\w\d\d\d)/$','coursePage'),
                      (r'^vote/(\w\w\d\d\d)/(.*?)/$','votePage'),
                      (r'^mylogin$','dev_login'),
                      (r'^profile/(.*?)/$','profilePage'),
                      (r'^api/vote/$','APIvote'),
                      (r'^api/makeComment/$','APImakeComment'),
                      (r'^api/getCourseTeacherScore/$','APIgetCourseTeacherScorePage'),
                      (r'^api/getCourseComment/$','APIgetCourseCommentPage'),
                      (r'^apidoc/$','APIdocPage'),
                      (r'^guestbook/$','guestbookPage'),
                      #(r'^sutuo/$', 'sutuoPage'),
                      #(r'^tuosou/$', 'sutuoPage'),
)
