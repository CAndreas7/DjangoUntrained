from django.test import TestCase, Client
from django.urls import reverse
from Management.models import User

class Test_UserEdit(TestCase):

    def setUp(self):

        self.client = Client()
        self.TA1 = User.objects.create(email="SomeUser1@user.com", password="testpassword", phone="", role=3)
        self.editURL = reverse('userEdit', kwargs={'email_id': self.TA1.email})

    def test_editEmail(self):
        self.client.post(self.editURL, {
            'email': "newEmail@user.com",
            'password': "testpassword",
            'fName': "Me",
            'lName': "not me",
            'phone': "",
            'role': 3,
        })
        self.assertEqual(User.objects.filter(email="SomeUser1@user.com").count(), 0,
                         "The previous unique email ID still exists.")
        self.assertEqual(User.objects.filter(email="newEmail@user.com").count(), 1,
                         "There are more than 1 user object with this unique ID")
        self.assertEqual(len(User.objects.all()), 1, "There should be a total of 1 User in the database.")


    def test_editPassword(self):
        self.client.post(self.editURL, {
            'email': 'SomeUser1@user.com',
            'fName': "Me",
            'lName': "not me",
            'password': "newpass",
            'phone': "123",
            'role': 3,
        })

        self.assertEqual(User.objects.filter(email="SomeUser1@user.com").count(), 1,
                         "There are more than 1 user object with this unique ID")

        self.assertEqual("newpass", User.objects.get(email="SomeUser1@user.com").password, "Password was not changed in"
                                                                                          "the forms correctly.")
        self.assertEqual(len(User.objects.all()), 1, "There should be a total of 1 User in the database.")
    def test_editPhone(self):
        self.client.post(self.editURL, {
            'email': 'SomeUser1@user.com',
            'fName': "Me",
            'lName': "not me",
            'password': "testpassword",
            'phone': '4143451234',
            'role': 3,
        })

        self.assertEqual(User.objects.filter(email="SomeUser1@user.com").count(), 1,
                         "There are more than 1 user object with this unique ID")
        self.assertEqual(User.objects.get(email="SomeUser1@user.com").phone, "4143451234", "Phone was not changed in"
                                                                                          "the forms correctly.")
        self.assertEqual(len(User.objects.all()), 1, "There should be a total of 1 User in the database.")
    def test_editRole(self):
        self.client.post(self.editURL, {
            'email': 'SomeUser1@user.com',
            'fName': "Me",
            'lName': "not me",
            'password': "testpassword",
            'phone': '4143451234',
            'role': 1,
        })
        self.assertEqual(User.objects.filter(email="SomeUser1@user.com").count(), 1,
                         "There are more than 1 user object with this unique ID")
        self.assertEqual(User.objects.get(email="SomeUser1@user.com").role, 1, "Role was not changed via "
                                                                                "forms correctly.")
        self.assertEqual(len(User.objects.all()), 1, "There should be a total of 1 User in the database.")

