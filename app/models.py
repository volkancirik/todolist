from django.db import models
from django.contrib.auth.models import User
from datetime import  datetime
from django.contrib import admin


class Day(models.Model):

    date = models.DateField()
    totalPoint = models.IntegerField(default= 0)
    dayClass =  models.IntegerField(default=1)

    def __unicode__(self):
        return str(self.date)

class Task(models.Model):
    taskClass = models.IntegerField(default=1)
    text = models.TextField(null=True)
    point = models.IntegerField(default=1)
    day = models.ForeignKey(Day)
    user = models.ForeignKey(User)
    create_date = models.DateTimeField(default=datetime.now())
    close_date = models.DateTimeField(null=True)
    def __unicode__(self):
        return self.text + ' ' + self.user.username




admin.site.register(Day)
admin.site.register(Task)