from django.db import models

# Create your models here.
# class User(models.Model):
#     uid = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=20)
#     email = models.CharField(max_length=40)
#     gender = models.CharField(max_length=6)
#     password = models.CharField(max_length=20)

class Admin(models.Model):
    aid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=20)

class Event(models.Model):
    eid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()
    duration = models.IntegerField()