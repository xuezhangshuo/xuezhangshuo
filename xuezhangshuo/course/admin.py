#coding: utf8

from django.contrib import admin
from xuezhangshuo.course.models import *

admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(CourseTeacher)
admin.site.register(Comment)
admin.site.register(Vote)
admin.site.register(CourseDescription)