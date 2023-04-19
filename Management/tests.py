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
