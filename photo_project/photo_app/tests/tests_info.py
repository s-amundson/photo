import logging

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..models import Gallery

logger = logging.getLogger(__name__)


class TestsInfo(TestCase):

    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_get_terms(self):
        response = self.client.get(reverse('photo:terms'), secure=True)
        self.assertTemplateUsed(response, 'photo_app/terms.html')
        self.assertEqual(response.status_code, 200)
        logging.debug(reverse('photo:terms'))

    def test_get_privacy(self):
        response = self.client.get(reverse('photo:privacy'), secure=True)
        self.assertTemplateUsed(response, 'photo_app/privacy.html')
        self.assertEqual(response.status_code, 200)
