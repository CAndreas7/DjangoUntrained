from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.

class User(models.Model):

    name = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    phone = models.IntegerField
    email = models.CharField(max_length=30)
    role = models.CharField(manx_length=20) #string match later  or models.ManyToManyField(roles))
    course = models.ManyToManyField(course)

class course(models.Model) :

    section = models.IntegerField()
    users = models.ManyToManyField(User)
    tasks = ArrayField(models.CharField(max_length=20))