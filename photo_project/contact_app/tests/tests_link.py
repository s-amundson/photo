import logging
import os
import tempfile

from django.conf import settings
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model


from ..models import Contact, Link

logger = logging.getLogger(__name__)


class TestsLink(TestCase):
    fixtures = ['f1']

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        self.User = get_user_model()
        self.client.force_login(self.User.objects.get(pk=1))
        self.contact = Contact.objects.create(first_name='John', email='john@example.com')

    def test_get_comment_noauth(self):
        self.client.logout()
        response = self.client.get(reverse('contact:link', kwargs={'contact_id': self.contact.id}), secure=True)
        self.assertEqual(response.status_code, 302)

    def test_get_comment_auth(self):
        response = self.client.get(reverse('contact:link', kwargs={'contact_id': self.contact.id}), secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'photo_app/form_as_p.html')

    def test_get_comment_exists(self):
        link = Link.objects.create(account='test acct', service='test service', person=self.contact)
        response = self.client.get(reverse('contact:link',
                                           kwargs={'contact_id': self.contact.id, 'link_id': link.id}),
                                   secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'photo_app/form_as_p.html')

    def test_post_link_good(self):
        response = self.client.post(reverse('contact:link', kwargs={'contact_id': self.contact.id}),
                                    {'account': 'test acct', 'service': 'test service', 'person': self.contact.id},
                                    secure=True)
        self.assertRedirects(response, reverse('contact:contact', kwargs={'contact_id': self.contact.id}))
        links = Link.objects.all()
        self.assertEqual(len(links), 1)
        contacts = Contact.objects.all()
        self.assertEqual(len(contacts), 1)
