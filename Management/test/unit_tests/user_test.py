import unittest
from Management.views import MyUser
from django.test import TestCase
from Management.models import *


class TestUser(TestCase):

    def setUp(self):
        self.user = User("testemail@uwm.edu", "testpassword", "", 1)
        self.user.save()
        self.supervisor = MyUser("testemail@uwm.edu", "testpassword", "", 1)
        # self.instructor = MyUser("secondemail@uwm.edu", "secret", "", 2)
        # self.ta = MyUser("taemail@uwm.edu", "mypass", "", 3)

    def test_getEmail(self):
        email = self.supervisor.getEmail()
        self.assertEqual(email, self.supervisor.email, msg="Returned username was not the user's username")

    def test_setEmail(self):
        self.supervisor.setEmail("myemail@uwm.edu")
        self.assertEqual(self.supervisor.email, "myemail@uwm.edu", msg="Username was not changed")

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

    def test_addAccount(self):
        self.supervisor.addAccount("email", "pass", "phone", 3)
        self.assertEqual(User.objects.filter(email="email").count(), 1, msg="No user exists with the given email")

    def test_editAccount(self):
        # from my understanding, this method should edit the user's own account
        # when a supervisor selects an account to edit, it selects an account, builds that user, and calls
        # THAT user's editAccount
        compAccount = User("taemail@uwm.edu", "newpass", "1(888)-999-0000", 3)
        compAccount.save()
        self.supervisor.editAccount("taemail@uwm.edu", "changedpass", "1(888)-999-0000", 3)
        self.assertEqual(User.objects.filter(password="changedpass").count(), 1, msg="Editted field did not match desired field")

    def test_removeAccount(self):
        user = User(email="deleteme@uwm.edu", password="goodbye", phone="", role=3)
        user.save()
        self.supervisor.removeAccount("deleteme@uwm.edu")
        self.assertEqual(User.objects.filter(email="deleteme@uwm.edu", password="goodbye").count(), 0,
                         msg="An account exists with the credentials that should have been deleted")

    def test_addCourse(self):
        course = Course(courseID=101, courseName="name", courseDescription="desc", courseDepartment="dept")
        course.save()
        self.supervisor.addCourse(101, "name", "desc", "dept")

        self.assertEqual(Course.objects.filter(courseID=101).count(), 1, msg="No course exists with the given courseID")

    def test_editCourse(self):
        course = Course(courseID=101, courseName="name", courseDescription="desc", courseDepartment="dept")
        course.save()
        self.supervisor.editCourse(101, "Algebra", "Entry level algebra", "Math")
        self.assertEqual(Course.objects.filter(courseName="Algebra").count(), 1, msg="Course was not updated in database")

    def test_removeCourse(self):
        course = Course(courseID=101, courseName="Algebra", courseDescription="Entry level college algebra",
                        courseDepartment="Math")
        course.save()
        self.supervisor.removeCourse(101)
        self.assertEqual(Course.objects.filter(courseID=101).count(), 0,
                         msg="A record exists with the primary key that should have been deleted")

    def test_addSection(self):
        course = Course(courseID=251, courseName="Intermediate Computer Programming",
                        courseDescription="A more advanced class that covers "
                                          "programming topics in greater "
                                          "depth", courseDepartment="CS")
        course.save()
        self.supervisor.addSection(800, "EMS100", "05:00PM", "07:00PM", 30, self.user, course)
        self.assertEqual(Section.objects.filter(sectionID=800).count(), 1,
                         msg="No section exists with the given sectionID")

    def test_editSection(self):
        course = Course(courseID=251, courseName="Intermediate Computer Programming",
                        courseDescription="A more advanced class that covers "
                                          "programming topics in greater "
                                          "depth", courseDepartment="CS")
        course.save()
        section = Section(sectionID=800, location="EMS100", startTime="05:00PM", endTime="07:00PM", capacity=30,
                          TA=self.user, courseID=course)
        section.save()
        self.supervisor.editSection(800, "EMS120", "05:00PM", "07:00PM", 30, self.user, course)
        self.assertEqual(Section.objects.filter(location="EMS120").count(), 1, msg="The section location was not changed")

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