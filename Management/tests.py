from django.test import TestCase
from django.test.runner import DiscoverRunner


class ManagementTests(TestCase):
    def test_all(self):
        test_runner = DiscoverRunner()
        test_runner.run_tests(['Management'])
