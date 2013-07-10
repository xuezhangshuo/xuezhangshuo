#coding:utf8

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
 
class xzsUserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
 
        user = self.model(
            email=xzsUserManager.normalize_email(email),
            name=name,
        )
 
        user.set_password(password)
        user.save(using=self._db)
        return user
 
    def create_superuser(self, email, name, password):
        user = self.create_user(email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class xzsUser(AbstractBaseUser):
	email = models.EmailField(verbose_name="邮箱", max_length=255, unique=True)
	name = models.CharField(verbose_name="姓名", max_length=30)
	RRid = models.CharField(max_length=15, blank=True)
	GENDER_CHOICES = (('M', '男'),('F', '女'),)
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	# portrait = models.ImageField(upload_to='photo', blank=True)
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['name']

	def get_full_name(self):
	    # For this case we return email. Could also be User.first_name User.last_name if you have these fields
	    return self.email
	
	def get_short_name(self):
	    # For this case we return email. Could also be User.first_name if you have this field
	    return self.email

	def has_perm(self, perm, obj=None):
	    # Handle whether the user has a specific permission?"
	    return True
	
	def has_module_perms(self, app_label):
	    # Handle whether the user has permissions to view the app `app_label`?"
	    return True

	@property
	def is_staff(self):
	    # Handle whether the user is a member of staff?"
	    return True

	objects = xzsUserManager()

	# def __unicode__(self):
		# return u'Profile of user: %s' % self.user.username
