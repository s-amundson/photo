import logging

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..models import Gallery, Release

logger = logging.getLogger(__name__)


class TestsGallery(TestCase):
    fixtures = ['f1']

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        self.User = get_user_model()
        self.test_user = self.User.objects.get(email='EmilyNConlan@einrot.com')
        self.client.force_login(self.test_user)

    def test_get_full_name(self):
        response = self.client.get(reverse('photo:gallery_view', kwargs={'gallery_id': 3}), secure=True)
        self.assertTemplateUsed(response, 'photo_app/gallery.html')
        self.assertFalse(response.context['owner'])
        self.assertEqual(len(response.context['models']), 1)
        self.assertEqual(response.context['models'][0]['name'], 'Rosalva Hall')
        logging.debug(response.context['models'][0]['name'])
        self.assertEqual(response.status_code, 200)

    def test_get_first_name(self):
        release = Release.objects.get(pk=1)
        release.use_full_name = False
        release.save()
        self.test_user = self.User.objects.get(pk=2)
        self.client.force_login(self.test_user)

        response = self.client.get(reverse('photo:gallery_view', kwargs={'gallery_id': 3}), secure=True)
        self.assertTemplateUsed(response, 'photo_app/gallery.html')
        self.assertFalse(response.context['owner'])
        self.assertEqual(len(response.context['models']), 1)
        self.assertEqual(response.context['models'][0]['name'], 'Rosalva')
        self.assertEqual(response.status_code, 200)

    def test_get_nick_name(self):
        release = Release.objects.get(pk=1)
        release.use_full_name = False
        release.use_first_name = False
        release.save()

        response = self.client.get(reverse('photo:gallery_view', kwargs={'gallery_id': 3}), secure=True)
        self.assertTemplateUsed(response, 'photo_app/gallery.html')
        self.assertFalse(response.context['owner'])
        self.assertEqual(len(response.context['models']), 1)
        self.assertEqual(response.context['models'][0]['name'], 'Rose')
        self.assertEqual(response.status_code, 200)

    def test_get_public(self):
        self.client.logout()
        response = self.client.get(reverse('photo:gallery_view', kwargs={'gallery_id': 2}), secure=True)
        self.assertTemplateUsed(response, 'photo_app/gallery.html')
        self.assertFalse(response.context['owner'])
        self.assertEqual(len(response.context['models']), 0)
        # self.assertEqual(response.context['models'][0]['name'], 'Rosalva Hall')
        # logging.debug(response.context['models'][0]['name'])
        self.assertEqual(response.status_code, 200)