import unittest
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from Management.forms import UserForm
from Management.models import *


# For whomever reads this:
# assertRaises can take in a tuple of exceptions rather than just asserting 1
# However, in order to determine WHICH exception is being raised, we split the tests
# To test, we can have if statements and use the "raise MYEXCEPTION" function
# Or we can HANDLE an exception to continue running
# LOOK AT THE LINK CHASE SENT
# https://www.geeksforgeeks.org/emailfield-django-models/
# line 266 in views
# In models, methods below initializer

class TestUser(TestCase):

    def setUp(self):
        self.user = User("testemail@uwm.edu", "test", "experiment", "testpassword", "", 1)
        self.user.save()
        self.supervisor = User("testemail@uwm.edu", "Visor", "Super", "password", "", 1)
        self.supervisor.save()
        # self.instructor = MyUser("secondemail@uwm.edu", "secret", "", 2)
        # self.ta = MyUser("taemail@uwm.edu", "mypass", "", 3)

    def test_getEmail(self):
        email = self.supervisor.getEmail()
        self.assertEqual(email, self.supervisor.email, msg="Returned username was not the user's username")

    def test_setEmail(self):
        self.supervisor.setEmail("myemail@uwm.edu")
        self.assertEqual(self.supervisor.email, "myemail@uwm.edu", msg="Username was not changed")

    def test_getFName(self):
        fName = self.supervisor.getfName()
        self.assertEqual(fName, self.supervisor.fName,
                         msg="First name field returned did not match the user's first name")

    def test_setNewFName(self):
        self.supervisor.setfName("Bo")
        self.assertEqual(self.supervisor.fName, "Bo", msg="User's first name was not updated")

    def test_setFName1(self):
        with self.assertRaises(ValidationError, msg="First name cannot be None"):
            self.supervisor.setfName(None)

    def test_setFName2(self):
        with self.assertRaises(ValidationError, msg="First name must be a String"):
            self.supervisor.setfName(1)

    def test_setFName3(self):
        with self.assertRaises(ValueError, msg="First name cannot be empty"):
            self.supervisor.setfName('')

    def test_getLName(self):
        lName = self.supervisor.getlName()
        self.assertEqual(lName, self.supervisor.lName,
                         msg="Last name field returned did not match the user's first name")

    def test_setLName1(self):
        pass

    def test_setLName2(self):
        pass

    def test_setLName3(self):
        pass

    def test_setLName4(self):
        pass

    def test_getPassword(self):
        password = self.supervisor.getPassword()
        self.assertEqual(self.supervisor.password, password, msg="getPassword did not grab the user's password")

    def test_setPassword(self):
        self.supervisor.setPassword("newpassword")
        self.assertEqual(self.supervisor.password, "newpassword", msg="Password was not changed")

    def test_getPhone(self):
        phone = self.supervisor.getPhone()
        self.assertEqual(self.supervisor.phone, phone, msg="getPhone did not grab the user's phone")

    def test_setPhone(self):
        self.supervisor.setPhone("1(111)-111-1111")
        self.assertEqual(self.supervisor.phone, "1(111)-111-1111", msg="setPhone was did not change user's phone")


class testAccount(TestCase):

    def setUp(self):
        self.user = User("testemail@uwm.edu", "test", "experiment", "testpassword", "", 1)
        self.user.save()
        self.supervisor = User("testemail@uwm.edu", "super", "visor", "password", "", 1)
        self.supervisor.save()

    def test_addAccount1(self):
        User.addAccount("email@uwm.edu", "User", "New", "pass", "333-499-2791", 3)
        self.assertEqual(User.objects.filter(email="email@uwm.edu").count(), 1,
                         msg="No user exists with the given email")

    def test_addAccount2(self):
        User.addAccount("testemail@uwm.edu", "Aid", "Teaching", "testpassword", "433-291-1173", 1)
        self.assertEqual(User.objects.filter(email="testemail@uwm.edu").count(), 1,
                         msg="this account already exists and should not have bee")

    def test_removeAccount1(self):
        user = User(email="deleteme@uwm.edu", lName="Bye", fName="Good", password="goodbye", phone="111-867-5309",
                    role=3)
        user.save()
        self.supervisor.removeAccount("deleteme@uwm.edu")
        self.assertEqual(User.objects.filter(email="deleteme@uwm.edu", password="goodbye").count(), 0,
                         msg="An account exists with the credentials that should have been deleted")

    def test_removeAccount2(self):
        with self.assertRaises(ObjectDoesNotExist, msg="No such account exists"):
            self.supervisor.removeAccount("myfakeemail@uwm.edu")


class editAccount(TestCase):

    def setUp(self):
        self.user = User("testemail@uwm.edu", "test", "experiment", "testpassword", "", 1)
        self.user.save()
        self.supervisor = User("testemail@uwm.edu", "Visor", "Super", "password", "", 1)
        self.supervisor.save()

    def test_TypeEmail1(self):
        with self.assertRaises(ValidationError, msg="email cannot be None, fails to raise TypeError"):
            self.supervisor.setEmail(None)

    def test_TypeEmail2(self):
        with self.assertRaises(ValidationError, msg="email not a char type data, fails to raise TypeError"):
            self.supervisor.setEmail(1)

    def test_typeEmail3(self):
        with self.assertRaises(ValidationError, msg="email not a char type data, fails to raise TypeError"):
            self.supervisor.setEmail(self.supervisor)

    def test_typeEmail4(self):
        with self.assertRaises(ValidationError, msg="Email must end with @uwm.edu"):
            self.supervisor.setEmail("email")

    def test_typePass1(self):
        with self.assertRaises(ValidationError, msg="Password cannot be None, fails to raise TypeError"):
            self.supervisor.setPassword(None)

    def test_typePass2(self):
        with self.assertRaises(ValidationError, msg="Password cannot be integer"):
            self.supervisor.setPassword(1)

    def test_typePass3(self):
        with self.assertRaises(ValidationError, msg="Password cannot be empty"):
            self.supervisor.setPassword("")

    def test_editPassword(self):
        self.supervisor.editAccount(self.supervisor.email, "changedpass", "1(888)-999-0000", 3)
        self.assertEqual(User.objects.filter(password="changedpass").count(), 1,
                         msg="Editted field did not match desired field")

    def test_typePhone1(self):
        with self.assertRaises(ValidationError, msg="Phone field cannot be None"):
            self.supervisor.setPhone(None)

    def test_typePhone2(self):
        with self.assertRaises(ValidationError, msg="Phone field cannot be an integer, must be a string"):
            self.supervisor.setPhone(12324498383)

    def test_editPhone(self):
        self.supervisor.editAccount(self.supervisor.email, self.supervisor.password, "1(449)-844-2323", 1)
        self.assertEqual(User.objects.filter(phone="1(449)-844-2323").count(), 1, msg="No account with given phone")

    def test_typeRole1(self):
        with self.assertRaises(ValidationError, msg="Field cannot be none"):
            self.supervisor.setRole(None)

    def test_typeRole2(self):
        with self.assertRaises(ValueError, msg="Role must be in range 1-3"):
            self.supervisor.setRole(0)

    def test_typeRole3(self):
        with self.assertRaises(ValueError, msg="Role must be in range 1-3"):
            self.supervisor.setRole(4)

    def test_editRole(self):
        self.supervisor.editAccount(self.supervisor.email, self.supervisor.password, self.supervisor.phone, 2)
        self.assertEqual(User.objects.filter(role=2).count(), 1, msg="No account with given role number")


class testCourseAddRemove(TestCase):

    def setUp(self):
        self.user = User("testemail@uwm.edu", "test", "experiment", "testpassword", "", 1)
        self.user.save()
        self.supervisor = User("testemail@uwm.edu", "Visor", "Super", "password", "", 1)
        self.supervisor.save()

    def test_addCourse(self):
        course = Course(courseID=101, courseName="name", courseDescription="desc", courseDepartment="dept")
        course.save()
        self.supervisor.addCourse(101, "name", "desc", "dept")

        self.assertEqual(Course.objects.filter(courseID=101).count(), 1, msg="No course exists with the given courseID")

    def test_removeCourse(self):
        course = Course(courseID=101, courseName="Algebra", courseDescription="Entry level college algebra",
                        courseDepartment="Math")
        course.save()
        self.supervisor.removeCourse(101)
        self.assertEqual(Course.objects.filter(courseID=101).count(), 0,
                         msg="A record exists with the primary key that should have been deleted")


class testEditCourse(TestCase):

    def setUp(self):
        self.user = User("testemail@uwm.edu", "test", "experiment", "testpassword", "", 1)
        self.user.save()
        self.supervisor = User("testemail@uwm.edu", "Visor", "Super", "password", "", 1)
        self.supervisor.save()
        self.course = Course(courseID=101, courseName="name", courseDescription="desc", courseDepartment="dept")
        self.course.save()

    def test_editCourseName(self):
        self.supervisor.editCourse(101, "Algebra", "Entry level algebra", "Math")
        self.assertEqual(Course.objects.filter(courseName="Algebra").count(), 1,
                         msg="Course was not updated in database")

    def test_editCourseName2(self):
        with self.assertRaises(ValidationError, msg="Course Name cannot be None"):
            self.supervisor.editCourse(101, None, "Entry level algebra", "Math")

    def test_editCourseName3(self):
        with self.assertRaises(ValidationError, msg="Course Name must be a String"):
            self.supervisor.editCourse(101, 1, "Entry level algebra", "Math")

    def test_editCourseName4(self):
        with self.assertRaises(ValidationError, msg="Course Name cannot be empty"):
            self.supervisor.editCourse(101, '', "Entry level algebra", "Math")

    def test_editCourseDesc(self):
        self.supervisor.editCourse(101, "Algebra", "An entry level college math class", "dept")
        self.assertEqual(Course.objects.filter(courseDescription="An entry level college math class").count(), 1,
                         msg="No course exists with the given description")

    def test_editCourseDesc2(self):
        with self.assertRaises(ValidationError, msg="Course Description cannot be None"):
            self.supervisor.editCourse(101, "Algebra", None, "dept")

    def test_editCourseDesc3(self):
        with self.assertRaises(ValidationError, msg="Course Description must be a String"):
            self.supervisor.editCourse(101, "Algebra", 1, "dept")

    def test_editCourseDesc4(self):
        with self.assertRaises(ValidationError, msg="Course Description cannot be empty"):
            self.supervisor.editCourse(101, "Algebra", '', "dept")

    def test_editCourseDepartment(self):
        self.supervisor.editCourse(101, "Algebra", "desc", "Math")
        self.assertEqual(Course.objects.filter(courseDepartment="Math").count(), 1,
                         msg="No such course with in the Math dept")

    def test_editCourseDepartment2(self):
        with self.assertRaises(ValidationError, msg="Course Department cannot be None"):
            self.supervisor.editCourse(101, "Algebra", "desc", None)

    def test_editCourseDepartment3(self):
        with self.assertRaises(ValidationError, msg="Course Department must be a String"):
            self.supervisor.editCourse(101, "Algebra", "desc", 1)

    def test_editCourseDepartment4(self):
        with self.assertRaises(ValidationError, msg="Course Department cannot be empty"):
            self.supervisor.editCourse(101, "Algebra", "desc", '')


class addRemoveSection(TestCase):

    def setUp(self):
        self.user = User("testemail@uwm.edu", "lastName", "firstName", "testpassword", "222-349-8283", 1)
        self.user.save()
        self.course = Course(courseID=251, courseName="Intermediate Computer Programming",
                             courseDescription="A more advanced class that covers "
                                               "programming topics in greater "
                                               "depth", courseDepartment="CS")
        self.course.save()
        self.supervisor = User("testemail@uwm.edu", "Visor", "Super", "testpassword", "123-499-6279", 1)
        self.supervisor.save()

    def test_addSection(self):
        self.supervisor.addSection(800, "EMS100", "05:00PM", "07:00PM", 30, self.user, self.course)
        self.assertEqual(Section.objects.filter(sectionID=800).count(), 1,
                         msg="No section exists with the given sectionID")

    def test_removeSection(self):
        course = Course(courseID=251, courseName="Intermediate Computer Programming",
                        courseDescription="A more advanced class that covers "
                                          "programming topics in greater "
                                          "depth", courseDepartment="CS")
        course.save()
        section = Section(sectionID=101, location="EMS100", startTime="05:00PM", endTime="07:00PM", capacity=30,
                          TA_id=self.supervisor.email, courseID_id=251)
        section.save()
        self.supervisor.removeSection(101)
        self.assertEqual(Section.objects.filter(sectionID=800).count(), 0,
                         msg="A section exists with the given sectionID")


class editSection(TestCase):
    def setUp(self):
        self.user = User("testemail@uwm.edu", "test", "experiment", "testpassword", "", 1)
        self.user.save()
        self.course = Course(courseID=251, courseName="Intermediate Computer Programming",
                             courseDescription="A more advanced class that covers "
                                               "programming topics in greater "
                                               "depth", courseDepartment="CS")
        self.course.save()
        self.section = Section(sectionID=800, location="EMS100", startTime="05:00PM", endTime="07:00PM", capacity=30,
                               TA=self.user, courseID=self.course)
        self.section.save()
        self.supervisor = User("testemail@uwm.edu", "visor", "super", "testpassword", "", 1)
        self.supervisor.save()

    def test_editLocation(self):
        self.supervisor.editSection(self.section.sectionID, "EMS120", self.section.startTime, self.section.endTime,
                                    self.section.capacity, self.user, self.course)
        self.assertEqual(Section.objects.filter(location="EMS120").count(), 1,
                         msg="The section location was not changed")

    def test_editLocation2(self):
        with self.assertRaises(ValidationError, msg="Location cannot be None"):
            self.supervisor.editSection(self.section.sectionID, None, self.section.startTime, self.section.endTime,
                                        self.section.capacity, self.user, self.course)

    def test_editLocation3(self):
        with self.assertRaises(ValidationError, msg="Location must be a String"):
            self.supervisor.editSection(self.section.sectionID, 1, self.section.startTime, self.section.endTime,
                                        self.section.capacity, self.user, self.course)

    def test_editLocation4(self):
        self.supervisor.editSection(self.section.sectionID, '', self.section.startTime, self.section.endTime,
                                    self.section.capacity, self.user, self.course)

    def test_editStartTime(self):
        self.supervisor.editSection(self.section.sectionID, self.section.location, "02:00PM", self.section.endTime,
                                    self.section.capacity, self.user, self.course)
        self.assertEqual(Section.objects.filter(startTime="02:00PM").count(), 1,
                         msg="The start time was not changed")

    def test_editStartTime2(self):
        with self.assertRaises(ValidationError, msg="StartTime cannot be None"):
            self.supervisor.editSection(self.section.sectionID, self.section.location, None, self.section.endTime,
                                        self.section.capacity, self.user, self.course)

    def test_editStartTime3(self):
        with self.assertRaises(ValidationError, msg="StartTime must be a String"):
            self.supervisor.editSection(self.section.sectionID, self.section.location, 1, self.section.endTime,
                                        self.section.capacity, self.user, self.course)

    def test_editStartTime4(self):
        with self.assertRaises(ValidationError, msg="StartTime cannot be empty"):
            self.supervisor.editSection(self.section.sectionID, self.section.location, '', self.section.endTime,
                                        self.section.capacity, self.user, self.course)

    def test_editEndTime(self):
        self.supervisor.editSection(self.section.sectionID, self.section.location, self.section.startTime, "07:30PM",
                                    self.section.capacity, self.user, self.course)
        self.assertEqual(Section.objects.filter(endTime="07:30PM").count(), 1,
                         msg="The end time was not changed")

    def test_editEndTime2(self):
        with self.assertRaises(ValidationError, msg="EndTime cannot be None"):
            self.supervisor.editSection(self.section.sectionID, self.section.location, self.section.startTime,
                                        None,
                                        self.section.capacity, self.user, self.course)

    def test_editEndTime3(self):
        with self.assertRaises(ValidationError, msg="EndTime must be a String"):
            self.supervisor.editSection(self.section.sectionID, self.section.location, self.section.startTime,
                                        1,
                                        self.section.capacity, self.user, self.course)

    def test_editEndTime4(self):
        with self.assertRaises(ValidationError, msg="EndTime cannot be empty"):
            self.supervisor.editSection(self.section.sectionID, self.section.location, self.section.startTime,
                                        '',
                                        self.section.capacity, self.user, self.course)

    def test_editCapacity(self):
        self.supervisor.editSection(self.section.sectionID, self.section.location, self.section.startTime,
                                    self.section.endTime,
                                    20, self.user, self.course)
        self.assertEqual(Section.objects.filter(capacity=20).count(), 1,
                         msg="The capacity was not changed")

    def test_editCapacity2(self):
        with self.assertRaises(ValidationError, msg="Capacity cannot be None"):
            self.supervisor.editSection(self.section.sectionID, self.section.location, self.section.startTime,
                                        self.section.endTime,
                                        None, self.user, self.course)

    def test_editCapacity3(self):
        with self.assertRaises(ValidationError, msg="Capacity must be an Integer"):
            self.supervisor.editSection(self.section.sectionID, self.section.location, self.section.startTime,
                                        self.section.endTime,
                                        "20", self.user, self.course)

    def test_editCapacity4(self):
        with self.assertRaises(ValidationError, msg="Capacity cannot be 0"):
            self.supervisor.editSection(self.section.sectionID, self.section.location, self.section.startTime,
                                        self.section.endTime,
                                        0, self.user, self.course)

    def test_editTA(self):
        newUser = User("taemail@uwm.edu", "Assistant", "Teaching", "tapass", "292-661-7322", 3)
        newUser.save()
        self.supervisor.editSection(self.section.sectionID, self.section.location, self.section.startTime,
                                    self.section.endTime,
                                    20, newUser, self.course)
        self.assertEqual(Section.objects.filter(TA=newUser).count(), 1,
                         msg="The TA was not changed")

    def test_editTA2(self):
        with self.assertRaises(ValidationError, msg="TA cannot be None"):
            self.supervisor.editSection(self.section.sectionID, self.section.location, self.section.startTime,
                                        self.section.endTime,
                                        20, None, self.course)

    def test_editTA3(self):
        with self.assertRaises(ValidationError, msg="TA must be a User object"):
            self.supervisor.editSection(self.section.sectionID, self.section.location, self.section.startTime,
                                        self.section.endTime,
                                        20, 1, self.course)

    def test_editTA4(self):
        with self.assertRaises(ValidationError, msg="TA must be a User object"):
            self.supervisor.editSection(self.section.sectionID, self.section.location, self.section.startTime,
                                        self.section.endTime,
                                        20, "taemail@uwm.edu", self.course)

    def test_editCourseID(self):
        newCourse = Course(361, "Intro to Software Development",
                           "A class that teaches the basics of software development", "CS")
        newCourse.save()
        self.supervisor.editSection(self.section.sectionID, self.section.location, self.section.startTime,
                                    self.section.endTime,
                                    self.section.capacity, self.section.TA, newCourse)
        self.assertEqual(Section.objects.filter(courseID=newCourse).count(), 1,
                         msg="No section exists with the new courseID")

    def test_editCourseID2(self):
        with self.assertRaises(ValidationError, msg="CourseID cannot be None"):
            self.supervisor.editSection(self.section.sectionID, self.section.location, self.section.startTime,
                                        self.section.endTime,
                                        self.section.capacity, self.section.TA, None)

    def test_editCourseID3(self):
        with self.assertRaises(ValidationError, msg="CourseID must be a Course Object"):
            self.supervisor.editSection(self.section.sectionID, self.section.location, self.section.startTime,
                                        self.section.endTime,
                                        self.section.capacity, self.section.TA, 1)

    def test_editCourseID4(self):
        with self.assertRaises(ValidationError, msg="CourseID cannot be None"):
            self.supervisor.editSection(self.section.sectionID, self.section.location, self.section.startTime,
                                        self.section.endTime,
                                        self.section.capacity, self.section.TA, "1")

    # def test_getAllCourses(self):
    #     all_courses = User.getAllCourses()
    #     self.assertEqual(all_courses, Course.objects.all(), msg="All courses should have been returned, but were not")


class testAddUserFromForm(TestCase):
    # class UserForm(forms.ModelForm):
    #     class Meta:
    #         model = User
    #         fields = ['email', 'lName', 'fName', 'password', 'phone', 'role']
    def setUp(self):
        self.form = UserForm({'email': "user@uwm.edu", 'lName': 'Boyland', 'fName': 'John', 'password': 'secret',
                              'phone': '299-341-7843', 'role': 2})
        self.badForm = UserForm({'email': "bozo", 'lName': 'Guy', 'fName': 'Random', 'password': 'nftethusiaust',
                              'phone': '999-867-5309', 'role': 3})
        self.user = User("testemail@uwm.edu", "test", "experiment", "testpassword", "", 1)
        self.user.save()
        # self.course = Course(courseID=251, courseName="Intermediate Computer Programming",
        #                      courseDescription="A more advanced class that covers "
        #                                        "programming topics in greater "
        #                                        "depth", courseDepartment="CS")
        # self.course.save()
        # self.section = Section(sectionID=800, location="EMS100", startTime="05:00PM", endTime="07:00PM", capacity=30,
        #                        TA=self.user, courseID=self.course)
        # self.section.save()
        self.supervisor = User("testemail@uwm.edu", "visor", "super", "testpassword", "", 1)
        self.supervisor.save()

    def test_userFromForm(self):
        # User.formAdd(self.form)
        self.assertEqual(User.formAdd(self.form), True, msg="User was not added from a form")

    def test_userFromFormBad(self):
        self.assertEqual(User.formAdd(self.badForm), False, msg="User is invalid, wasn't listed as such")


