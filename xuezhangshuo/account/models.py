#coding:utf8

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
	name = models.CharField(max_length=30)
    portrait = models.ImageField(upload_to='photo', blank=True)
    RRid = models.CharField(max_length=15)
    user = models.ForeignKey(User, unique=True)
    GENDER_CHOICES = (('M', '男'),('F', '女'),)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __unicode__(self):
        return u'Profile of user: %s' % self.user.username
