import unittest
from Management.models import User
from django.test import TestCase

class TestUser:

    def setUp(self):
        self.supervisor = User("testemail@uwm.edu", "testpassword", "", 1)
        self.instructor = User("secondemail@uwm.edu", "secret", "", 2)
        self.ta = User("taemail@uwm.edu", "mypass", "", 3)

    def test_getUsername(self):
        username = self.supervisor.getUsername()
        self.assertEquals(username, self.supervisor.email, msg="Returned username was not the user's username")

    def test_setUsername(self):
        pass

    def test_getPassword(self):
        pass

    def test_setPassword(self):
        pass

    def test_getPhone(self):
        pass

    def test_setPhone(self):
        pass

    def test_addAccount(self):
        pass

    def test_editAccount(self):
        pass

    def test_removeAccount(self):
        pass

    def test_addCourse(self):
        pass

    def test_editCourse(self):
        pass

    def test_removeCourse(self):
        pass

    def test_addSection(self):
        pass

    def test_editSection(self):
        pass

    def test_removeSection(self):
        pass
