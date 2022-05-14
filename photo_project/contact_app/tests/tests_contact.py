import logging
import os
import tempfile

from django.conf import settings
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model


from ..models import Contact

logger = logging.getLogger(__name__)


class TestsContact(TestCase):
    fixtures = ['f1']

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        self.User = get_user_model()
        self.client.force_login(self.User.objects.get(pk=1))

    def test_get_contact_noauth(self):
        self.client.logout()
        response = self.client.get(reverse('contact:contact'), secure=True)
        self.assertEqual(response.status_code, 302)

    def test_get_contact_auth(self):
        response = self.client.get(reverse('contact:contact'), secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact_app/contact.html')

    def test_get_contact_exists(self):
        Contact.objects.create(first_name='John', email='john@example.com')
        response = self.client.get(reverse('contact:contact'), secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact_app/contact.html')

    def test_post_contact_good(self):
        d = {'first_name': 'John', 'email': 'john@example.com', 'is_model': True, 'score': 3}
        response = self.client.post(reverse('contact:contact'), d, secure=True)

        self.assertRedirects(response, reverse('contact:contact_list'))
        contacts = Contact.objects.all()
        self.assertEqual(len(contacts), 1)
