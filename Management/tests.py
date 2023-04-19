from django.test import TestCase, Client
from django.urls import reverse
from .models import User


class LoginTests(TestCase):
    def setUp(self):
        # set user credentials
        self.client = Client()
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)

    def testLogin(self):
        # send login
        response = self.client.post(reverse('login'), self.credentials, follow=True)
        # check if logged in
        self.assertTrue(response.context['user'].is_active)


class LoginFail(TestCase):
    #create a good user
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='gooduser', password='goodpass')

    def testBadPass(self):
        response = self.client.login(username='gooduser', password='badpass')
        self.assertFalse(response)
    def testBadUser(self):
        response = self.client.login(username='baduser', password='goodpass')
        self.assertFalse(response)


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
