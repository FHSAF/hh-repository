from django.test import TestCase
from .models import Site, Page, ExceptedPages

class SiteTestCase(TestCase):
    def setUp(self):
        Site.objects.create(name="Testname", url="http://test.com")
        Site.objects.create(name="Testname1", url="http://test1.com")

    def test_Sites(self):
        """Sites that have url and name are correctly identified"""
        site1 = Site.objects.get(name="Testname")
        site2 = Site.objects.get(url="http://test1.com")
        self.assertEqual(site1.url, 'http://test.com')
        self.assertEqual(site2.name, 'Testname1')