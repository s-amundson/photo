import logging
import os

from PIL import Image
from django.conf import settings
from django.db.models import Q
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.datetime_safe import date

from ..models import Images, Gallery

logger = logging.getLogger(__name__)


class TestsGalleryList(TestCase):
    fixtures = ['f1']

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        self.User = get_user_model()
        self.test_user = self.User.objects.get(email='EmilyNConlan@einrot.com')
        # self.test_user = self.User.objects.create_user(username='fred', password='secret')

    def test_get_no_auth(self):
        response = self.client.get(reverse('photo:index'), secure=True)
        self.assertEqual(len(response.context['gallery_list']), 1)
        self.assertEqual(response.status_code, 200)

    def test_get_auth1(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('photo:index'), secure=True)
        self.assertEqual(len(response.context['gallery_list']), 5)
        self.assertEqual(response.status_code, 200)

    def test_get_auth2(self):
        self.client.force_login(self.User.objects.get(pk=2))
        response = self.client.get(reverse('photo:index'), secure=True)
        self.assertEqual(len(response.context['gallery_list']), 2)
        self.assertEqual(response.status_code, 200)


        # g = Gallery(is_public=False, name='test', owner=self.test_user, photo_model=None,
        #             public_date=None, shoot_date='2021-06-26')
        # # with open() as f:
        # p = os.path.join(settings.BASE_DIR, 'photo_app', 'fixtures', '1.jpeg')
        # # p = "/home/sam/PycharmProjects/photo/photo_project/photo_app/static/images/target2.png"
        # logging.debug(p)
        # img = Image.open(p)
