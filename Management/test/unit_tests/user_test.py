from Management.models import User
from django.test import TestCase


class TestUser(TestCase):

    def setUp(self):
        self.supervisor = User("testemail@uwm.edu", "testpassword", "", 1)
        self.instructor = User("secondemail@uwm.edu", "secret", "", 2)
        self.ta = User("taemail@uwm.edu", "mypass", "", 3)

    def test_getUsername(self):
        username = self.supervisor.getUsername()
        self.assertEqual(username, self.supervisor.email, msg="Returned username was not the user's username")

    def test_setUsername(self):
        self.supervisor.setUsername("myemail@uwm.edu")
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
        newAcc = User(email="email", password="pass", phone="phone", role=3)
        self.assertEqual(User.objects.filter(email="email", password="pass"), newAcc)

    def test_editAccount(self):
        self.supervisor.editAccount("")

    def test_removeAccount(self):
        user = User.objects.create("deleteme@uwm.edu", "goodbye", "", 3)
        self.supervisor.removeAccount("deleteme@uwm.edu")
        self.assertEqual(User.objects.filter(email="deleteme@uwm.edu", password="goodbye").len(), 0,
                         msg="An account exists with the credentials that should have been deleted")

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
