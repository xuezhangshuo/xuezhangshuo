from django.db import models

# Create your models here.

class SutuoItem(models.Model):
    filename = models.CharField(max_length=100)
    classID = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    studentID = models.CharField(max_length=20)
    score = models.CharField(max_length=20)
    itemID = models.CharField(max_length=20)
    
    def __unicode__(self):
        return self.name