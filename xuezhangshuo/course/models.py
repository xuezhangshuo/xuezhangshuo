#coding: utf8
from django.db import models
from django.conf import settings

class Teacher(models.Model):
    name = models.CharField(max_length=30)
    staffID = models.CharField(max_length=20)
    GENDER_CHOICES = (('M', '男'),('F', '女'),)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    
    def __unicode__(self):
        return self.name
    
class Course(models.Model):
    courseID = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=50)
    teachers = models.ManyToManyField(Teacher,through='CourseTeacher')
    
    def __unicode__(self):
        return self.name
        
class CourseTeacher(models.Model):
    teacher = models.ForeignKey(Teacher)
    course = models.ForeignKey(Course)
    rank = models.IntegerField() #should be a float filed !!!
    rank_cnt = models.IntegerField()
    # year = models.IntegerField()
    
    def __unicode__(self):
        return u"%s %s" % (self.course.courseID,self.teacher.name)
    
# class User(models.Model):
#     RRid = models.CharField(max_length=15)
#     name = models.CharField(max_length=30)
#     avatar = models.CharField(max_length=120)
#     access_token = models.CharField(max_length=100)
    
#     def __unicode__(self):
#         return self.name
    
class Comment(models.Model):
    course_teacher = models.ForeignKey(CourseTeacher)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    comment = models.CharField(max_length=400)
    datetime = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return u'%s: %s' % (self.user.name,self.comment)

class Vote(models.Model):
    course_teacher = models.ForeignKey(CourseTeacher)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    value = models.IntegerField()
    datetime = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return u'%s %s %s' % (self.user.name,self.course_teacher.course.name,self.course_teacher.teacher.name)

class CourseDescription(models.Model):
    content = models.CharField(max_length=4000)
    modified_time = models.DateTimeField(auto_now=True)
    course = models.ForeignKey(Course)
    contributors = models.ManyToManyField(settings.AUTH_USER_MODEL)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return u'%s' % (self.course.name)

# class Message(models.Model):
#     sender = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='sender')
#     reciever = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='reciever')
#     content = models.CharField(max_length=400)
#     datetime = models.DateTimeField(auto_now=True)

#     def __unicode__(self):
#         return u'%s %s' % (self.sender.name,self.content)
