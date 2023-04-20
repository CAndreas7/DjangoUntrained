from django.test import TestCase, Client
from Management.models import User


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
        self.assertContains(response, '/mainHome', msg_prefix="The response should let you through to /base i think.")

    def testBadLogin(self):
        response = self.client.post("/", {
            'email': 'testuser@uwm.edu',
            'password': 'badpass'},
            follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '/', msg_prefix="make sure it stays in home")

    def testNonExistentUser(self):
        response = self.client.post('/', {
            'email': 'IDontExisit@gmail.com',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please enter a correct email and password.')

    def testMissingEmail(self):
        response = self.client.post('/', {
            'email': '',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')

    def testMissingPassword(self):
        response = self.client.post('/', {
            'email': 'testuser',
            'password': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')