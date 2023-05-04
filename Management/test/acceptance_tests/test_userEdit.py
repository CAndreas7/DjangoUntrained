from django.test import TestCase, Client
from Management.models import User

class Test_UserEdit(TestCase):

    def setUp(self):

        self.client = Client()
        self.TA1 = User.objects.create(email="SomeUser@user.com", password="testpassword", phone="", role=3)

    def test_editEmail(self):
        self.client.post('/userEdit/', {
            'email': 'newEmail@user.com'
        })
        self.assertEqual(User.objects.filter(email="SomeUser@user.com").count(), 0,
                         "The previous unique email ID still exists.")
        self.assertEqual(User.objects.filter(email="newEmail@user.com").count(), 1,
                         "There are more than 1 user object with this unique ID")
        self.assertEqual(len(User.objects.all()), 1, "There should be a total of 1 User in the database.")


    def test_editPassword(self):
        self.client.post('/userEdit/', {
            'password': 'newpass'
        })
        #checks to see if there is one user object with its Unique ID
        self.assertEqual(User.objects.filter(email="newEmail@user.com").count(), 1,
                         "There are more than 1 user object with this unique ID")
        self.assertEqual(User.objects.get(email="newEmail@user.com").password, "newpass", "Password was not changed in"
                                                                                          "the forms correctly.")
        self.assertEqual(len(User.objects.all()), 1, "There should be a total of 1 User in the database.")
    def test_editPhone(self):
        self.client.post('/userEdit/', {
            'phone': '414-345-1234'
        })
        self.assertEqual(User.objects.filter(email="newEmail@user.com").count(), 1,
                         "There are more than 1 user object with this unique ID")
        self.assertEqual(User.objects.get(email="newEmail@user.com").phone, "414-345-1234", "Phone was not changed in"
                                                                                          "the forms correctly.")
        self.assertEqual(len(User.objects.all()), 1, "There should be a total of 1 User in the database.")
    def test_editRole(self):
        self.client.post('/userEdit/', {
            'role': '1'
        })
        self.assertEqual(User.objects.filter(email="newEmail@user.com").count(), 1,
                         "There are more than 1 user object with this unique ID")
        self.assertEqual(User.objects.get(email="newEmail@user.com").role, "1", "Role was not changed via "
                                                                                "forms correctly.")
        self.assertEqual(len(User.objects.all()), 1, "There should be a total of 1 User in the database.")

