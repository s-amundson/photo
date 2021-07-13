import logging

from django.test import TestCase, Client
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

    def test_get(self):
        response = self.client.get(reverse('photo:gallery_view', kwargs={'gallery_id': 3}), secure=True)
        self.assertTemplateUsed(response, 'photo_app/gallery.html')
        self.assertEqual(response.status_code, 200)