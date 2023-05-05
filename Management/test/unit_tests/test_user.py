import unittest
from Management.views import MyUser
from django.test import TestCase
from Management.models import *


class TestUser(TestCase):

    def setUp(self):
        self.user = User("testemail@uwm.edu", "Wayne", "Bruce", "testpassword", "", 1)
        self.user.save()
        self.supervisor = MyUser("testemail@uwm.edu", "Kent", "Clark", "testpassword", "", 1)

        # self.instructor = MyUser("secondemail@uwm.edu", "secret", "", 2)
        # self.ta = MyUser("taemail@uwm.edu", "mypass", "", 3)

    def test_getEmail(self):
        email = self.supervisor.getEmail()
        self.assertEqual(email, self.supervisor.email, msg="Returned username was not the user's username")

    def test_setEmail(self):
        self.supervisor.setEmail("myemail@uwm.edu")
        self.assertEqual(self.supervisor.email, "myemail@uwm.edu", msg="Username was not changed")

    def test_getlName(self):
        name = self.user.getlName()
        self.assertEqual(self.user.lName, name, msg="Returned last name was not the user's last name")

    def test_setlName(self):
        self.user.setlName("Dickinson")
        self.assertEqual("Dickinson", self.user.lName, msg="Last name was not set correctly.")

    def test_getfName(self):
        name = self.user.getfName()
        self.assertEqual(self.user.fName, name, msg="Returned first name was not the user's first name")

    def test_setfName(self):

        self.user.setfName("Thomas")
        self.assertEqual("Thomas", self.user.fName, msg="First name was not set correctly.")

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
        self.user = User("testemail@uwm.edu", "testpassword", "", 1)
        self.user.save()
        self.supervisor = MyUser("testemail@uwm.edu", "testpassword", "", 1)

    def test_addAccount(self):
        self.supervisor.addAccount("email", "pass", "phone", 3)
        self.assertEqual(User.objects.filter(email="email").count(), 1, msg="No user exists with the given email")

    def test_removeAccount(self):
        user = User(email="deleteme@uwm.edu", password="goodbye", phone="", role=3)
        user.save()
        self.supervisor.removeAccount("deleteme@uwm.edu")
        self.assertEqual(User.objects.filter(email="deleteme@uwm.edu", password="goodbye").count(), 0,
                         msg="An account exists with the credentials that should have been deleted")


class editAccount(TestCase):

    def setUp(self):
        self.user = User("testemail@uwm.edu", "testpassword", "", 1)
        self.user.save()
        self.supervisor = MyUser("testemail@uwm.edu", "testpassword", "", 1)

    def test_editPassword(self):
        self.supervisor.editAccount(self.supervisor.email, "changedpass", "1(888)-999-0000", 3)
        self.assertEqual(User.objects.filter(password="changedpass").count(), 1,
                         msg="Editted field did not match desired field")

    def test_editPhone(self):
        self.supervisor.editAccount(self.supervisor.email, self.supervisor.password, "1(449)-844-2323", 1)
        self.assertEqual(User.objects.filter(phone="1(449)-844-2323").count(), 1, msg="No account with given phone")

    def test_editRole(self):
        self.supervisor.editAccount(self.supervisor.email, self.supervisor.password, self.supervisor.phone, 2)
        self.assertEqual(User.objects.filter(role=2).count(), 1, msg="No account with given role number")


class testCourseAddRemove(TestCase):

    def setUp(self):
        self.user = User("testemail@uwm.edu", "testpassword", "", 1)
        self.user.save()
        self.supervisor = MyUser("testemail@uwm.edu", "testpassword", "", 1)

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
        self.user = User("testemail@uwm.edu", "testpassword", "", 1)
        self.user.save()
        self.supervisor = MyUser("testemail@uwm.edu", "testpassword", "", 1)
        self.course = Course(courseID=101, courseName="name", courseDescription="desc", courseDepartment="dept")
        self.course.save()

    def test_editCourseName(self):
        self.supervisor.editCourse(101, "Algebra", "Entry level algebra", "Math")
        self.assertEqual(Course.objects.filter(courseName="Algebra").count(), 1,
                         msg="Course was not updated in database")

    def test_editCourseDesc(self):
        self.supervisor.editCourse(101, "Algebra", "An entry level college math class", "dept")
        self.assertEqual(Course.objects.filter(courseDescription="An entry level college math class").count(), 1,
                         msg="No course exists with the given description")

    def test_editCourseDept(self):
        self.supervisor.editCourse(101, "Algebra", "desc", "Math")
        self.assertEqual(Course.objects.filter(courseDepartment="Math").count(), 1,
                         msg="No such course with in the Math dept")

class addRemoveSection(TestCase):

    def setUp(self):
        self.user = User("testemail@uwm.edu", "testpassword", "", 1)
        self.user.save()
        self.course = Course(courseID=251, courseName="Intermediate Computer Programming",
                             courseDescription="A more advanced class that covers "
                                               "programming topics in greater "
                                               "depth", courseDepartment="CS")
        self.course.save()
        self.supervisor = MyUser("testemail@uwm.edu", "testpassword", "", 1)

    def test_addSection(self):
        self.supervisor.addSection(800, "EMS100", "05:00PM", "07:00PM", 30, self.user, self.course)
        self.assertEqual(Section.objects.filter(sectionID=800).count(), 1,
                         msg="No section exists with the given sectionID")

    def test_removeSection(self):
        course = Course(courseID=251, courseName="Intermediate Computer Programming",
                        courseDescription="A more advanced class that covers "
                                          "programming topics in greater "
                                          "depth", courseDepartment="CS")
        course.save(0)
        section = Section(sectionID=101, location="EMS100", startTime="05:00PM", endTime="07:00PM", capacity=30,
                          TA_id=self.supervisor.email, courseID_id=251)
        self.supervisor.removeSection(800)
        self.assertEqual(Section.objects.filter(sectionID=800).count(), 0,
                         msg="A section exists with the given sectionID")


class editSection(TestCase):
    def setUp(self):
        self.user = User("testemail@uwm.edu", "testpassword", "", 1)
        self.user.save()
        self.course = Course(courseID=251, courseName="Intermediate Computer Programming",
                             courseDescription="A more advanced class that covers "
                                               "programming topics in greater "
                                               "depth", courseDepartment="CS")
        self.course.save()
        self.section = Section(sectionID=800, location="EMS100", startTime="05:00PM", endTime="07:00PM", capacity=30,
                          TA=self.user, courseID=self.course)
        self.section.save()
        self.supervisor = MyUser("testemail@uwm.edu", "testpassword", "", 1)

    def test_editLocation(self):
        self.supervisor.editSection(self.section.sectionID, "EMS120", self.section.startTime, self.section.endTime,
                                    self.section.capacity, self.user, self.course)
        self.assertEqual(Section.objects.filter(location="EMS120").count(), 1,
                         msg="The section location was not changed")

    def test_editStartTime(self):
        self.supervisor.editSection(self.section.sectionID, self.section.location, "02:00PM", self.section.endTime,
                                    self.section.capacity, self.user, self.course)
        self.assertEqual(Section.objects.filter(startTime="02:00PM").count(), 1,
                         msg="The section location was not changed")

    def test_editEndTime(self):
        self.supervisor.editSection(self.section.sectionID, self.section.location, self.section.startTime, "07:30PM",
                                    self.section.capacity, self.user, self.course)
        self.assertEqual(Section.objects.filter(endTime="07:30PM").count(), 1,
                         msg="The section location was not changed")

    def test_editCapacity(self):
        self.supervisor.editSection(self.section.sectionID, self.section.location, self.section.startTime, self.section.endTime,
                                    20, self.user, self.course)
        self.assertEqual(Section.objects.filter(capacity=20).count(), 1,
                         msg="The section location was not changed")

    def test_editTA(self):
        newUser = User("taemail@uwm.edu", "tapass", "", 3)
        newUser.save()
        self.supervisor.editSection(self.section.sectionID, self.section.location, self.section.startTime, self.section.endTime,
                                    20, newUser, self.course)
        self.assertEqual(Section.objects.filter(TA=newUser).count(), 1,
                         msg="The section location was not changed")

    def test_newCourseID(self):
        newCourse = Course(361, "Intro to Software Development", "A class that teaches the basics of software development", "CS")
        newCourse.save()
        self.supervisor.editSection(self.section.sectionID, self.section.location, self.section.startTime, self.section.endTime,
                                    self.section.capacity, self.section.TA, newCourse)
        self.assertEqual(Section.objects.filter(courseID = newCourse).count(), 1, msg="No section exists with the new courseID")