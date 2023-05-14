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
        self.deleteInstr1URL = reverse('userDelete', kwargs={'email_id': self.Instructor1.email})
        self.accountInfoURL = reverse('users')

    def test_display(self):
        response = self.client.get(self.accountInfoURL)
        """WORKS IF ROLE SESSION DIDNT EXISTS. NICE!
        
        """
        queryset_users = response.context['results']
        list = []
        for user in queryset_users:
            list.append(user)
        self.assertEqual(list[0].email, "SomeUser1@user.com", "Course 1 is not being displayed")
        self.assertEqual(list[1].email, "SomeUser2@user.com", "Course 2 is not being displayed")
        self.assertEqual(list[2].email, "SomeUser3@user.com", "Course 2 is not being displayed")

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

        ##role Session makes this blow up as well.

        self.client.get(self.deleteInstr1URL)

        self.assertEqual(0, User.objects.filter(email="SomeUser3@user.com").count(), "The user was not deleted from the"
                                                                                     "database")
