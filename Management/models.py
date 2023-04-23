from django.db import models

# Create your models here.
"""
class Course(models.Model) :

    section = models.IntegerField()
    #users = models.ManyToManyField(User) #an array that string match username|email or how User objects
    #tasks = ArrayField(models.CharField(max_length=20))
class User(models.Model):

    name = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    phone = models.IntegerField()
    email = models.CharField(max_length=30)
    role = models.CharField(max_length=20) #string match later  or models.ManyToManyField(roles))
    course = models.ManyToManyField(Course)

"""


# This is the User table, which stores information about the users
# The email (UWM) is the primary key, but the login method should match
# the password field to the correct email
class User(models.Model):
    # specifying primary_key=True disables the default ID field
    email = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    # this is a way I found of representing in the DB the role a user is
    # the person creating the account with add in a 1, 2, or 3
    # and see Supervisor/Instructor/TA in the DB in the admin page
    role = models.PositiveSmallIntegerField(
        choices=(
            (1, "Supervisor"),
            (2, "Instructor"),
            (3, "TA")
        ))

    def __init__(self, email, password, phone, role):
        self.email = email
        self.password = password
        self.phone = phone
        self.role = role


# This is the Course table, which stores information about a Course at a university
# The only necessary field is: courseID
class Course(models.Model):
    # specifying primary_key=True disables the default ID field
    courseID = models.IntegerField(primary_key=True)
    courseName = models.CharField(max_length=40)
    courseSections = models.ForeignKey('Section', on_delete=models.SET_NULL())
    # VVVV  These 2 fields below may not be necessary, included for appearance
    courseDescription = models.CharField(max_length=140)
    courseDepartment = models.CharField(max_length=16)

    def __int__(self, ID, name, description, department):
        self.courseID = ID
        self.courseName = name
        self.courseDescription = description
        self.courseDepartment = department

    def getName(self):
        return self.courseName

    def setName(self, name):
        self.courseName = name

    def getDescription(self):
        return self.courseDescription

    def setDescription(self, description):
        self.courseDescription = description

    def getDepartment(self):
        return self.courseDepartment

    def setDepartment(self, department):
        self.courseDepartment = department

    #def addSection(self):



# This is the Section table, to reference a LAB section for a course.
# The only NECESSARY fields are:  sectionID, TA, and courseID
#
class Section(models.Model):
    sectionID = models.IntegerField(primary_key=True)
    # building and room number like EMS180
    location = models.CharField(max_length=8)
    # these 2 would be formatted "11:00AM
    startTime = models.CharField(max_length=7)
    endTime = models.CharField(max_length=7)
    capacity = models.IntegerField()
    # this references a value in Courses, when a TA/User is deleted
    # the section will remain and this field becomes Null
    TA = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # since this is intrinsically tied to Courses, when a course is deleted
    # the section shouldn't exist anymore, so we delete this section
    courseID = models.ForeignKey(Course, on_delete=models.CASCADE)

    # this is a junction table, showing a user assigned to a course
    # A user can be assigned multiple courses, and a course can have multiple users assigned
    # this should have an intrinsic, auto incrementing ID field in Django
    # When a course is deleted, the assignment doesn't exist anymore
    # When a user is deleted, the assignment doesn't exist anymore


class UsersToCourse(models.Model):
    courseID = models.ForeignKey(Course, on_delete=models.CASCADE)
    assignment = models.ForeignKey(User, on_delete=models.CASCADE)