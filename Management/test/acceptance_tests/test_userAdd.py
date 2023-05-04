from django.test import TestCase, Client
from Management.models import User

class Test_UserAdd(TestCase):

    def setUp(self):
        self.client = Client()
        self.TA1 = User.objects.create(email="SomeUser@user.com", password="testpassword", phone="", role=3)

    def test_addNewUser(self):
        self.client.post('/userAdd/', {
            'email': 'newEmail@user.com',
            'password': "somepass",
            'phone': '123456789',
            'role': 1
        })
        self.assertEqual(User.objects.filter(email="newEmail@user.com").count(), 1,
                         "The new user was not created via forms properly.")
        self.assertEqual(len(User.objects.all()), 2, "There should be a total of 2 Users in the database.")

    def test_addSameUser(self):
        self.client.post('/userAdd/', {
            'email': 'SomeUser@user.com',
            'password': "testpassword",
            'phone': '',
            'role': 3
        })
        self.assertEqual(User.objects.filter(email="SomeUser@user.com").count(), 1,
                         "The added same user was either deleted or added twice.")
        self.assertEqual(len(User.objects.all()), 1, "There should be a total of 1 User in the database.")
    def test_addSameEmail(self):
        self.client.post('/userAdd/', {
            'email': 'SomeUser@user.com',
            'password': "test",
            'phone': '1231',
            'role': 2
        })
        self.assertEqual(User.objects.filter(email="SomeUser@user.com").count(), 1,
                         "The added same user that contained a Unique ID already in the database"
                         " was either deleted or added twice.")
        self.assertEqual(len(User.objects.all()), 1, "There should be a total of 1 User in the database.")


