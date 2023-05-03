from django.test import TestCase, Client
from Management.models import Course


class Test_SectionPage(TestCase):
    def setUp(self):
        self.client = Client()

    def test_editSection(self):
        pass
    def test_removeSection(self):
        pass
    def test_goToAddSection(self):
        pass
