from django.test import SimpleTestCase
from django.urls import reverse, resolve
from orphanage.views import *


class TestUrls(SimpleTestCase):
    """
        We use SimpleTestCase when we don't want to interact with the database
    """

    def test_children_url_is_resolved(self):
        url = reverse('orphanage:children')
        self.assertEquals(resolve(url).func, children)

    def test_child_insert_url_is_resolved(self):
        url = reverse('orphanage:child_insert')
        self.assertEquals(resolve(url).func, child_insert)
