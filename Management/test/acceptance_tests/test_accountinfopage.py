from django.test import TestCase, Client
from django.urls import reverse
from Management.models import User

class Test_AccountInfoPage(TestCase):
    def setUp(self):
        self.client = Client()
        self.TA1 = User.objects.create(email="SomeUser1@user.com", password="testpassword", phone="", role=3)
        self.Supervisor1 = User.objects.create(email="SomeUser2@user.com", password="testpassword", phone="", role=1)
        self.Instructor1 = User.objects.create(email="SomeUser3@user.com", password="testpassword", phone="", role=2)

        self.userAddURL = reverse('userAdd')
        self.TA1EditURL = reverse('userEdit', kwargs={'email_id': self.TA1.email})
        #this page doesn't exist, You get a role error.
        self.deleteInstr1URL = reverse('userDelete', kwargs={'email_id': self.Instructor1.email})


    def test_add_user_link(self):
        response = self.client.get(self.userAddURL)

        self.assertEqual(response.status_code, 200, "Status code is not 200")
        self.assertTemplateUsed(response, 'main/User/userAdd.html')

    def test_edit_user_link(self):
        response = self.client.get('/userEdit/SomeUser1@user.com/')
        print(self.TA1EditURL)
        self.assertEqual(response.status_code, 200, "Status code is not 200")
        self.assertTemplateUsed(response, 'main/User/userEdit.html')
    def test_deleteInstructor1(self):
        self.client.get(self.deleteInstr1URL)

        self.assertEqual(0, User.objects.filter(email="SomeUser3@user.com").count(), "The user was not deleted from the"
                                                                                     "database")
