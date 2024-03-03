import logging

from django.test import TestCase, Client, tag
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..models import Gallery

logger = logging.getLogger(__name__)


class TestsGallery(TestCase):
    fixtures = ['f1']

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        self.User = get_user_model()
        self.test_user = self.User.objects.get(email='EmilyNConlan@einrot.com')
        self.client.force_login(self.test_user)

    # @tag('temp')
    def test_get_authenticated(self):
        response = self.client.get(reverse('photo:gallery_view', kwargs={'gallery_id': 3}), secure=True)
        self.assertTemplateUsed(response, 'photo_app/gallery.html')
        self.assertFalse(response.context['owner'])
        self.assertEqual(response.status_code, 200)

    # @tag('temp')
    def test_get_private(self):
        user = self.User.objects.get(pk=2)
        self.client.force_login(user)

        gallery = Gallery.objects.get(pk=4)
        gallery.privacy_level = 'private'
        # gallery.owner = self.User.objects.get(pk=3)
        gallery.save()

        response = self.client.get(reverse('photo:gallery_view', kwargs={'gallery_id': 4}), secure=True)
        self.assertTemplateUsed(response, 'photo_app/gallery.html')
        self.assertFalse(response.context['owner'])
        self.assertEqual(response.status_code, 200)

    @tag('denied')
    def test_get_private_denied(self):
        user = self.User.objects.get(pk=3)
        self.client.force_login(user)

        gallery = Gallery.objects.get(pk=3)
        gallery.privacy_level = 'private'
        gallery.owner = self.test_user
        gallery.save()

        response = self.client.get(reverse('photo:gallery_view', kwargs={'gallery_id': 3}), secure=True)
        self.assertEqual(response.status_code, 403)

    # @tag('temp')
    def test_get_public(self):
        self.client.logout()
        response = self.client.get(reverse('photo:gallery_view', kwargs={'gallery_id': 2}), secure=True)
        self.assertTemplateUsed(response, 'photo_app/gallery.html')
        self.assertFalse(response.context['owner'])
        self.assertEqual(response.status_code, 200)