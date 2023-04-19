from django.test import TestCase, Client
from django.urls import reverse
from .models import User


class LoginTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(email='testuser@uwm.edu', password='testpass', role='1')

    def testGoodLogin(self):
        response = self.client.post('/', {
            'email': 'testuser@uwm.edu',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 302, "The status code should be 302 for a good login")
        self.assertContains(response, '/base', msg_prefix="The response should let you through to /base i think.")

    def testBadLogin(self):
        response = self.client.post("/", {
            'email': 'testuser@uwm.edu',
            'password': 'badpass'},
            follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '/', msg_prefix="make sure it stays in home")


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
