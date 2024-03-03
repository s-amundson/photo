import logging

from django.test import TestCase, Client, tag
from django.urls import reverse
from django.contrib.auth import get_user_model


logger = logging.getLogger(__name__)


class TestsGalleryList(TestCase):
    fixtures = ['f1']

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        self.User = get_user_model()
        self.test_user = self.User.objects.get(email='EmilyNConlan@einrot.com')
        # self.test_user = self.User.objects.create_user(username='fred', password='secret')

    # @tag('temp')
    def test_get_no_auth(self):
        response = self.client.get(reverse('photo:index'), secure=True)
        self.assertEqual(len(response.context['gallery_list']), 1)
        self.assertEqual(response.status_code, 200)

    # @tag('temp')
    def test_get_auth1(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('photo:index'), secure=True)
        self.assertEqual(len(response.context['gallery_list']), 5)
        self.assertEqual(response.status_code, 200)

    # @tag('temp')
    def test_get_auth2(self):
        self.client.force_login(self.User.objects.get(pk=2))
        response = self.client.get(reverse('photo:index'), secure=True)
        self.assertEqual(len(response.context['gallery_list']), 3)
        self.assertEqual(response.status_code, 200)
