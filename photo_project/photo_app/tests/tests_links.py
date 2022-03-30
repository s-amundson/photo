import logging
import os

from django.conf import settings
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..models import Links

logger = logging.getLogger(__name__)


class TestsLinks(TestCase):
    fixtures = ['f1']

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        self.User = get_user_model()
        self.test_user = self.User.objects.get(pk=2)
        self.client.force_login(self.test_user)

    def test_get_link_form_no_id(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('photo:links_form'), secure=True)

        self.assertEqual(response.status_code, 200)

    def test_get_link_form_id(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('photo:links_form', kwargs={'link_id': 1}), secure=True)
        # logging.debug(response.context)
        self.assertEqual(response.status_code, 200)

    def test_post_link_form_noid(self):
        self.client.force_login(self.test_user)
        self.client.post(reverse('photo:links_form'),
                                    {'category': ['2'], 'url': ['http://rose.ig.example.com']}, secure=True)
        l = Links.objects.all()
        self.assertEqual(len(l), 2)
        self.assertEqual(l[1].url, 'http://rose.ig.example.com')

    def test_post_link_form_id(self):
        self.client.force_login(self.test_user)
        self.client.post(reverse('photo:links_form', kwargs={'link_id': 1}),
                                    {'category': ['2'], 'url': ['http://rose.ig.example.com']}, secure=True)
        l = Links.objects.all()
        self.assertEqual(len(l), 1)
        self.assertEqual(l[0].url, 'http://rose.ig.example.com')

    def test_post_link_form_noid_invalid(self):
        self.client.force_login(self.test_user)
        self.client.post(reverse('photo:links_form'), {'url': ['http://rose.ig.example.com']}, secure=True)
        l = Links.objects.all()
        self.assertEqual(len(l), 1)

    def test_get_link_table_id(self):
        self.client.force_login(self.test_user)
        response = self.client.get('/links_table/2/', secure=True)
        # logging.debug(response.context)
        self.assertEqual(response.status_code, 200)

    def test_get_link_table_bad_id(self):
        self.client.force_login(self.test_user)
        response = self.client.get('/links_table/10/', secure=True)
        # logging.debug(response.context)
        self.assertEqual(response.status_code, 404)

    def test_catgory_add(self):
        self.client.force_login(self.User.objects.get(pk=1))
        response = self.client.get(reverse('photo:link_category-add'), secure=True)

        self.assertEqual(response.status_code, 200)

    def test_catgory_update(self):
        self.client.force_login(self.User.objects.get(pk=1))
        response = self.client.get(reverse('photo:link_category-update', kwargs={'pk': 1}), secure=True)

        self.assertEqual(response.status_code, 200)
        'link_category-add'