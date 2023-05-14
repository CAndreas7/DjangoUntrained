from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.validators import EmailValidator
from django.shortcuts import render, redirect, get_object_or_404
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
    email = models.EmailField(max_length=20, primary_key=True)
    lName = models.CharField(max_length=30, null=True, default='')
    fName = models.CharField(max_length=30, null=True, default='')
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

    def addAccount(self, email, lname, fname, password, phone, role):
        if User.objects.filter(email=email).count() == 0:
            if email is None or password is None or phone is None or role is None:
                raise ValidationError("Email cannot be None")
            if not isinstance(email, str):
                raise ValidationError("Email must be of type String")  # split
            if not isinstance(lname, str):
                raise ValidationError("Last Name must be a String")
            if not isinstance(fname, str):
                raise ValidationError("First Name must be a String")
            if not isinstance(password, str):
                raise ValidationError("Password must by a String")
            if not isinstance(phone, str):
                raise ValidationError("Phone number must be a String")
            if not isinstance(role, int):
                raise ValidationError("Role must be entered as an Integer")
            if password.__len__() < 1:
                raise ValidationError("Password cannot be empty")
            email_validator = EmailValidator(allowlist="uwm.edu")
            email_validator.__call__(email)
            user = User(email=email, lName=lname, fName=fname, password=password, phone=phone, role=role)
            user.save()

    def getEmail(self):
        return self.email

    def setEmail(self, email):
        if email is None:
            raise ValidationError("Email cannot be None")
        if not isinstance(email, str):
            raise ValidationError("Email must be of type String")
        email_validator = EmailValidator(allowlist="uwm.edu")
        email_validator.__call__(email)

        # user = User.objects.get(email=self.email)
        # user.email = email
        # user.save()
        # for user in users:
        #     user.email = email
        #     user.save()
        self.email = email

    def getlName(self):
        return self.lName

    def setlName(self, name):
        if name is None:
            raise ValidationError("name cannot be None")
        if not isinstance(name, str):
            raise ValidationError("Name must be of type String")
        if name.__len__() == 0:
            raise ValueError("Name cannot be empty")

        self.lName = name

    def getfName(self):
        return self.fName

    def setfName(self, name):
        if name is None:
            raise ValidationError("Last name cannot be None")
        if not isinstance(name, str):
            raise ValidationError("Last Name must be of type String")
        if name.__len__() == 0:
            raise ValueError("Last Name cannot be empty")

        self.fName = name

    def getPassword(self):
        return self.password

    def setPassword(self, password):
        if password is None:
            raise ValidationError("password cannot be None")
        if not isinstance(password, str):
            raise ValidationError("password must be type String")
        if password.__len__() < 1:
            raise ValidationError("password cannot be empty")

        user = User.objects.get(password=self.password)
        user.password = password
        user.save()
        self.password = password

    def getPhone(self):
        return self.phone

    def setPhone(self, phoneNum):
        if phoneNum is None:
            raise ValidationError("New PhoneNum cannot be None")
        if not isinstance(phoneNum, str):
            raise ValidationError("New PhoneNum must be type String")
        user = User.objects.get(phone=self.phone)
        user.phone = phoneNum
        user.save()
        self.phone = phoneNum

    def getRole(self):
        role = self.role
        if role == 1:
            return "Supervisor"
        elif role == 2:
            return "Instructor"
        elif role == 3:
            return "TA"
        return

    def setRole(self, role):
        if role is None:
            raise ValidationError("Role cannot be None")
        if not isinstance(role, int):
            raise ValidationError("Role must be of type int")
        if role < 1 or role > 3:
            raise ValueError("Role must be in the range 1 through 3")

        user = User.objects.get(email=self.email)
        user.role = role
        user.save()
        self.role = role

    def editAccount(self, email, password, phoneNum, role):
        if User.objects.filter(email=email):
            user = User.objects.get(email=email)
            user.setPassword(password)
            user.setPhone(phoneNum)
            user.setRole(role)
            self.password = password
            self.phone = phoneNum
            self.role = role
        else:
            raise ObjectDoesNotExist("No such account to edit")

    def removeAccount(self, email):
        if User.objects.filter(email=email).count() == 0:
            raise ObjectDoesNotExist("No such account to remove")
        else:
            User.objects.get(email=email).delete()
            # self.email = None
            # self.password = None
            # self.phone = None
            # self.role = None

    def addCourse(self, courseID, courseName, courseDesc, courseDept):
        course = Course(courseID=courseID, courseName=courseName, courseDescription=courseDesc,
                        courseDepartment=courseDept)
        course.save()

    def editCourse(self, courseID, courseName, courseDescription, courseDepartment):
        #       courses = Course.objects.filter(courseID=courseID)
        if Course.objects.filter(courseID=courseID).count() == 1:
            if courseName is None:
                raise ValidationError("Course Name cannot be None")
            if not isinstance(courseName, str):
                raise ValidationError("Course Name must be a String")
            if courseName.__len__() == 0:
                raise ValidationError("Course Name cannot be empty")
            if courseDescription is None:
                raise ValidationError("Course Description cannot be None")
            if not isinstance(courseDescription, str):
                raise ValidationError("Course Description must be a String")
            if courseDescription.__len__() == 0:
                raise ValidationError("Course Description cannot be empty")
            if courseDepartment is None:
                raise ValidationError("Course Department cannot be None")
            if not isinstance(courseDepartment, str):
                raise ValidationError("Course Department must be a String")
            if courseDepartment.__len__() == 0:
                raise ValidationError("Course Department cannot be empty")

            courses = Course.objects.get(courseID=courseID)
            courses.courseName = courseName
            courses.courseDescription = courseDescription
            courses.courseDepartment = courseDepartment
            courses.save()

        # for item in courses:
        #     item.courseName = courseName
        #     item.courseDescription = courseDescription
        #     item.courseDepartment = courseDepartment
        #     item.save()

    def removeCourse(self, courseID):
        Course.objects.filter(courseID=courseID).delete()

    def addSection(self, sectionID, location, startTime, endTime, capacity, ta, courseID):
        section = Section(sectionID=sectionID, location=location, startTime=startTime, endTime=endTime,
                          capacity=capacity, TA=ta, courseID=courseID)
        section.save()

    def editSection(self, sectionID, location, startTime, endTime, capacity, ta, courseID):
        if Section.objects.filter(sectionID=sectionID).count() == 1:
            if location is None:
                raise ValidationError("Location cannot be None")
            if not isinstance(location, str):
                raise ValidationError("Location must be of type String")
            if startTime is None:
                raise ValidationError("StartTime cannot be None")
            if not isinstance(startTime, str):
                raise ValidationError("StartTime must be of type String")
            if startTime.__len__() == 0:
                raise ValidationError("StartTime cannot be empty")
            if endTime is None:
                raise ValidationError("EndTime cannot be None")
            if not isinstance(endTime, str):
                raise ValidationError("EndTime must be of type ")
            if endTime.__len__() == 0:
                raise ValidationError("EndTime cannot be empty")
            if capacity is None:
                raise ValidationError("Capacity cannot be None")
            if not isinstance(capacity, int):
                raise ValidationError(" must be of type ")
            if capacity < 1:
                raise ValidationError("Capacity must be greater than 1")
            if ta is None:
                raise ValidationError("TA cannot be None")
            if not isinstance(ta, User):
                raise ValidationError("TA must be of type ")
            if courseID is None:
                raise ValidationError("CourseID cannot be None")
            if not isinstance(courseID, Course):
                raise ValidationError("CourseID must be of type ")
            section = Section.objects.get(sectionID=sectionID)
            section.location = location
            section.startTime = startTime
            section.endTime = endTime
            section.capacity = capacity
            section.TA = ta
            section.courseID = courseID
            section.save()

        # for item in sections:
        #     item.location = location
        #     item.startTime = startTime
        #     item.endTime = endTime
        #     item.capacity = capacity
        #     item.TA_id = ta
        #     item.courseID_id = courseID
        #     item.save()

    def removeSection(self, sectionID):
        Section.objects.filter(sectionID=sectionID).delete()

    @staticmethod
    def formAdd(form):

        if form.is_valid():
            email = form.cleaned_data['email']
            fname = form.cleaned_data['fName']
            lname = form.cleaned_data['lName']
            password = form.cleaned_data['password']
            phone = form.cleaned_data['phone']
            role = form.cleaned_data['role']

            # Create a new User object with the extracted data
            user = User(email=email, fName=fname, lName=lname, password=password, phone=phone, role=role)
            user.save()
            return True
        return False

    @staticmethod
    def getUser(email):
        return get_object_or_404(User, pk=email)

    @staticmethod
    def deleteUser(email):
        User.objects.filter(email=email).delete()


# This is the Course table, which stores information about a Course at a university
# The only necessary field is: courseID
class Course(models.Model):
    # specifying primary_key=True disables the default ID field
    courseID = models.IntegerField(primary_key=True)
    courseName = models.CharField(max_length=40)
    # VVVV  These 2 fields below may not be necessary, included for appearance
    courseDescription = models.CharField(max_length=140)
    courseDepartment = models.CharField(max_length=16)

    def getName(self):
        return self.courseName

    def setName(self, name):
        if name is None:
            raise ValidationError("Course Name cannot be None")
        if not isinstance(name, str):
            raise ValidationError("Course Name must be type String")
        if name.__len__() == 0:
            raise ValidationError("Course Name cannot be empty")

        self.courseName = name

    def getDescription(self):
        return self.courseDescription

    def setDescription(self, description):
        if description is None:
            raise ValidationError("Description cannot be None")
        if not isinstance(description, str):
            raise ValidationError("Description must be type String")
        if description.__len__() == 0:
            raise ValidationError("Description cannot be empty")

        self.courseDescription = description

    def getDepartment(self):
        return self.courseDepartment

    def setDepartment(self, department):
        if department is None:
            raise ValidationError("Department cannot be None")
        if not isinstance(department, str):
            raise ValidationError("Department must be type String")
        if department.__len__() == 0:
            raise ValidationError("Department entry cannot be empty")
        self.courseDepartment = department

    @staticmethod
    def formAdd(form):

        if form.is_valid():
            courseID = form.cleaned_data['courseID']
            courseName = form.cleaned_data['courseName']
            courseDescription = form.cleaned_data['courseDescription']
            courseDepartment = form.cleaned_data['courseDepartment']

            # Create a new Course object with the extracted data
            course = Course(courseID=courseID, courseName=courseName, courseDescription=courseDescription,
                            courseDepartment=courseDepartment)

            # Save the new course to the database
            course.save()
            return True
        else:
            return False

    def formSave(self, form):

        if form.is_valid():
            form.save()
            return True
        else:
            return False

    @staticmethod
    def getCourse(courseID):
        return get_object_or_404(Course, pk=courseID)


    def removeCourse(self):
        ThisCourse = Course.objects.get(courseID=self.courseID)
        ThisCourse.delete()

    @staticmethod
    def getAll():
        return Course.objects.all()

    # def addSection(self):


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


    def getID(self):
        # Return the section ID
        return self.sectionID

    def getLocation(self):
        return self.location

    def setLocation(self, location):
        self.location = location

    def getStart(self):
        return self.startTime

    def setStart(self, start):
        self.startTime = start

    def getEnd(self):
        return self.endTime

    def setEnd(self, end):
        self.endTime = end

    def getCapacity(self):
        return self.capacity

    def setCapacity(self, capacity):
        self.capacity = capacity

    def getTA(self):
        return self.TA

    def setTA(self, ta):
        self.TA = ta

    def getCourseID(self):
        return self.courseID

    def setCourseID(self, course):
        self.courseID = course

    def getCourseName(self):
        return Course.objects.get(courseID=self.courseID).getName()
    @staticmethod
    def getSectionsFromCourse(courseID):
        return Section.objects.filter(courseID=courseID)

    # def setID(self, new_id):
    #     # Update the section ID
    #     self.sectionID = new_id
    #     self.save()

    # def add(self):
    #     self.save()
    @staticmethod
    def formAdd(form, courseID):
        if form.is_valid():
            location = form.cleaned_data['location']
            startTime = form.cleaned_data['startTime']
            endTime = form.cleaned_data['endTime']
            capacity = form.cleaned_data['capacity']
            TA = form.cleaned_data['TA']
            sectionID = form.cleaned_data['sectionID']

            # Create a new Section object with the extracted data
            section = Section(sectionID=sectionID, location=location, startTime=startTime, capacity=capacity, TA=TA,
                              courseID=Course.objects.get(pk=courseID), endTime=endTime)
            section.save()
            return True
        else:
            return False, form.errors

    def formSave(self, form):
        if form.is_valid():
            self.setLocation(form.cleaned_data['location'])
            self.setStart(form.cleaned_data['startTime'])
            self.setEnd(form.cleaned_data['endTime'])
            self.setCapacity(form.cleaned_data['capacity'])
            self.setTA(form.cleaned_data['TA'])
            self.save()
            return True
        else:
            return False, form.errors

    @staticmethod
    def getSection(sectionID):
        return get_object_or_404(Section, pk=sectionID)

    @staticmethod
    def deleteSection(sectionID):
        Section.objects.filter(sectionID=sectionID).delete()

# this is a junction table, showing a user assigned to a course
# A user can be assigned multiple courses, and a course can have multiple users assigned
# this should have an intrinsic, auto incrementing ID field in Django
# When a course is deleted, the assignment doesn't exist anymore
# When a user is deleted, the assignment doesn't exist anymore
class UsersToCourse(models.Model):
    assignment = models.CharField(max_length=20)
    courseID = models.IntegerField()

    def getUser(self):
        return User.objects.get(pk=self.assignment)

    def getCourse(self):
        return Course.objects.get(pk=self.courseID)

    def removeUser(self):
        UserTo = UsersToCourse.objects.get(courseID=self.courseID, assignment=self.assignment)
        UserTo.delete()

    @staticmethod
    def getUserToCourse(courseID):
        return UsersToCourse.objects.filter(courseID=courseID)

    @staticmethod
    def getUserCourses(email):
        return UsersToCourse.objects.filter(assignment=email)

    @staticmethod
    def addUserToCourse(email, courseID):
        userTo = UsersToCourse(courseID=courseID, assignment=email)
        userTo.save()
        return userTo

    @staticmethod
    def delCourseUsers(courseID):
        utcQuery = UsersToCourse.getUserToCourse(courseID)
        for x in utcQuery:
            x.removeUser()

    @staticmethod
    def delUserCourses(email):
        utcQuery = UsersToCourse.getUserCourses(email)
        for x in utcQuery:
            x.removeUser()