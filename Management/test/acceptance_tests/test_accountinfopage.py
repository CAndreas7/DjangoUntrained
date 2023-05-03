from django.test import TestCase, Client
from Management.models import User

class Test_AccountInfoPage(TestCase):
    def setUp(self):
        self.client = Client()
        self.TA1 = User.objects.create(email="SomeUser1@user.com", password="testpassword", phone="", role=3)
        self.Supervisor1 = User.objects.create(email="SomeUser2@user.com", password="testpassword", phone="", role=1)
        self.Instructor1 = User.objects.create(email="SomeUser3@user.com", password="testpassword", phone="", role=2)

    def test_add_user_link(self):
        pass
    def test_edit_user_link(self):
        pass
    def test_delete_user_link(self):
        pass