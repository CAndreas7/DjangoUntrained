from django.test import TestCase, Client
from .models import User


class LoginTests(TestCase):
    """
    user = None
    credentials = None

    def setUp(self):
        self.user = Client()
        # trying to set up a database with a user's full fields from the DB
        #
        self.credentials = {"one": ["", "", "", 1], "two": ["", "", "", 2], "three": ["", "", "", 3]}

        for i in self.credentials.keys():
            # not sure if this is the correct way to grab from the dictionary
            temp = User(email=i, password=i, phone=i, role=i)
            temp.save()

    def test_correctName(self):
        for i in self.credentials.keys():
            resp = self.user.post("/", {"name": i, "password": i}, follow=True)
            self.assertEqual(resp.context["name"], i, "name not passed from login to list")

    def test_complete(self):
        pass
"""

class LoginFail(TestCase):
    pass


class CreateAccount(TestCase):
    pass


class CreateCourse(TestCase):
    pass


class CreateSection(TestCase):
    pass


class DeleteAccount(TestCase):
    pass


class DeleteCourse(TestCase):
    pass


class DeleteSection(TestCase):
    pass
