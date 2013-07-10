#coding: utf8
from django.db import models
from django.contrib.auth.models import User

class Teacher(models.Model):
    name = models.CharField(max_length=30)
    staffID = models.CharField(max_length=20)
    GENDER_CHOICES = (('M', '男'),('F', '女'),)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    
    def __unicode__(self):
        return self.name
    
class Course(models.Model):
    courseID = models.CharField(max_length=6)
    name = models.CharField(max_length=50)
    teachers = models.ManyToManyField(Teacher,through='CourseTeacher')
    
    def __unicode__(self):
        return self.name
        
class CourseTeacher(models.Model):
    teacher = models.ForeignKey(Teacher)
    course = models.ForeignKey(Course)
    recommend = models.IntegerField()
    teaching_skill = models.IntegerField()
    grades_level = models.IntegerField()
    voteCnt = models.IntegerField()
    total_score = models.IntegerField()
    
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
    course = models.ForeignKey(Course)
    teacher = models.ManyToManyField(Teacher)
    course_teacher = models.ManyToManyField(CourseTeacher)
    user = models.ForeignKey(User)
    comment = models.CharField(max_length=400)
    datetime = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return u'%s: %s' % (self.user.name,self.comment)

class Vote(models.Model):
    course = models.ForeignKey(Course)
    teacher = models.ForeignKey(Teacher)
    course_teacher = models.ForeignKey(CourseTeacher)
    user = models.ForeignKey(User)
    teaching_skill = models.IntegerField()
    grades_level = models.IntegerField()
    
    def __unicode__(self):
        return u'%s %s' % (self.user.name,self.teacher.name)

class Message(models.Model):
    sender = models.ForeignKey(User,related_name='sender')
    reciever = models.ForeignKey(User,related_name='reciever')
    content = models.CharField(max_length=400)
    datetime = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'%s %s' % (self.sender.name,self.content)
