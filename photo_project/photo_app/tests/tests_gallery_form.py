import logging

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..models import Gallery

logger = logging.getLogger(__name__)


class TestsGalleryForm(TestCase):
    fixtures = ['f1']

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        self.User = get_user_model()
        self.test_user = self.User.objects.get(email='EmilyNConlan@einrot.com')
        self.client.force_login(self.test_user)
        self.test_dict = {'name': 'name', 'shoot_date': '2020-02-02', 'is_mature': False, 'is_public': True,
                          'photographer': self.test_user.id, 'public_date': '2020-03-03'}
        # self.test_user = self.User.objects.create_user(username='fred', password='secret')

    def test_get_new(self):
        response = self.client.get(reverse('photo:gallery_form'), secure=True)
        self.assertTemplateUsed(response, 'photo_app/forms/gallery_form.html')
        self.assertEqual(response.status_code, 200)

    def test_get_exists_not_owner(self):
        self.client.force_login(self.User.objects.get(pk=2))
        response = self.client.get(reverse('photo:gallery_form', kwargs={'gallery_id': 3}), secure=True)
        # self.assertTemplateUsed(response, 'photo_app/forms/gallery_form.html')
        self.assertEqual(response.status_code, 400)

    def test_get_exists_owner(self):
        response = self.client.get(reverse('photo:gallery_form', kwargs={'gallery_id': 4}), secure=True)
        self.assertTemplateUsed(response, 'photo_app/forms/gallery_form.html')
        self.assertEqual(response.status_code, 200)

    def test_get_auth1(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('photo:index'), secure=True)
        self.assertEqual(len(response.context['gallery_list']), 5)
        self.assertEqual(response.status_code, 200)

    def test_get_auth2(self):
        self.client.force_login(self.User.objects.get(pk=2))
        response = self.client.get(reverse('photo:index'), secure=True)
        self.assertEqual(len(response.context['gallery_list']), 3)
        self.assertEqual(response.status_code, 200)

    def test_post_new(self):
        response = self.client.post(reverse('photo:gallery_form'), self.test_dict, secure=True)
        self.assertEqual(response.status_code, 200)
        g = Gallery.objects.all()
        self.assertEqual(len(g), 6)
        g = g[5]
        self.assertEqual(g.name, 'name')
        self.assertTrue(g.is_public)

    def test_post_update_authorized(self):
        response = self.client.post(reverse('photo:gallery_form', kwargs={'gallery_id': 4}), self.test_dict, secure=True)
        self.assertEqual(response.status_code, 200)
        g = Gallery.objects.all()
        self.assertEqual(len(g), 5)
        g = Gallery.objects.get(pk=4)
        self.assertEqual(g.name, 'name')
        self.assertTrue(g.is_public)

    def test_post_update_unauthorized(self):
        self.client.force_login(self.User.objects.get(pk=2))
        response = self.client.post(reverse('photo:gallery_form', kwargs={'gallery_id': 4}), self.test_dict,
                                    secure=True)
        self.assertEqual(response.status_code, 400)
        g = Gallery.objects.all()
        self.assertEqual(len(g), 5)
        g = Gallery.objects.get(pk=4)
        self.assertEqual(g.name, 'Four')
        self.assertTrue(g.is_public)


class TestsGalleryFormApi(TestCase):
    fixtures = ['f1']

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        self.User = get_user_model()
        self.test_user = self.User.objects.get(email='EmilyNConlan@einrot.com')
        self.client.force_login(self.test_user)
        self.test_dict = {'name': 'name', 'shoot_date': '2020-02-02', 'is_mature': False, 'is_public': True,
                          'photographer': self.test_user.id, 'photo_model': 2, 'public_date': '2020-03-03'}
        # self.test_user = self.User.objects.create_user(username='fred', password='secret')

    def test_post_new(self):
        response = self.client.post(reverse('photo:gallery_form_api'), self.test_dict, secure=True)
        self.assertEqual(response.status_code, 200)
        g = Gallery.objects.all()
        self.assertEqual(len(g), 6)
        g = g[5]
        self.assertEqual(g.name, 'name')
        self.assertTrue(g.is_public)

    def test_post_update_authorized(self):
        response = self.client.post(reverse('photo:gallery_form', kwargs={'gallery_id': 4}), self.test_dict, secure=True)
        self.assertEqual(response.status_code, 200)
        g = Gallery.objects.all()
        self.assertEqual(len(g), 5)
        g = Gallery.objects.get(pk=4)
        self.assertEqual(g.name, 'name')
        self.assertTrue(g.is_public)

    def test_post_update_unauthorized(self):
        self.client.force_login(self.User.objects.get(pk=2))
        response = self.client.post(reverse('photo:gallery_form', kwargs={'gallery_id': 4}), self.test_dict,
                                    secure=True)
        self.assertEqual(response.status_code, 400)
        g = Gallery.objects.all()
        self.assertEqual(len(g), 5)
        g = Gallery.objects.get(pk=4)
        self.assertEqual(g.name, 'Four')
        self.assertTrue(g.is_public)
