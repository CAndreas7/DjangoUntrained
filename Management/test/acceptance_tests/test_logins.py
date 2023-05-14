from django.test import TestCase, Client
from Management.models import User


class LoginTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(email='testuser@uwm.edu', password='testpass', role='1')
        self.user.save()

    def testGoodLogin(self):
        response = self.client.post('/', {
            'email': 'testuser@uwm.edu',
            'password': 'testpass'},
            follow=True)
        self.assertRedirects(response, "/main/", status_code=302, target_status_code=200, fetch_redirect_response=True)

    def testBadLogin(self):
        response = self.client.post("/", {
            'email': 'testuser@uwm.edu',
            'password': 'badpass'},
            follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['message'], "Incorrect Password")


    def testNonExistentUser(self):
        response = self.client.post('/', {
            'email': 'IDontExisit@gmail.com',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['message'], "Please enter a correct email and password.")

    def testMissingEmail(self):
        response = self.client.post('/', {
            'email': '',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['message'], 'Email required.')
        self.assertEqual(response.context['password'], 'testpass')

    def testMissingPassword(self):
        response = self.client.post('/', {
            'email': 'testuser',
            'password': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['message'], 'Password required.', "error message is incorrect")
        self.assertEqual(response.context['person'], 'testuser', "email was not autofilled")

    def testMissingEmailAndPassword(self):
        response = self.client.post('/', {
            'email': '',
            'password': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['message'], 'Email and password required.', "error message is incorrect")