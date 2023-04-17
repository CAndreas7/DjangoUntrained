from django.db import models

# Create your models here.
class Course(models.Model) :

    section = models.IntegerField()
    #users = models.ManyToManyField(User)
    #tasks = ArrayField(models.CharField(max_length=20))
class User(models.Model):

    name = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    phone = models.IntegerField()
    email = models.CharField(max_length=30)
    role = models.CharField(max_length=20) #string match later  or models.ManyToManyField(roles))
    course = models.ManyToManyField(Course)

