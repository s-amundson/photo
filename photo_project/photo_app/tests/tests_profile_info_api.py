import logging

from PIL import Image
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..models import User

logger = logging.getLogger(__name__)


class TestsProfileInfoApi(TestCase):
    fixtures = ['fixture_photo_model_api']

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        User = get_user_model()
        self.test_user = User.objects.get(email='EmilyNConlan@einrot.com')
        # self.test_user = User.objects.create_user(username='fred', password='secret')
        self.client.force_login(self.test_user)
        self.user_dict = {'first_name': 'Emily', 'last_name': 'Conlan', "dob": "1995-12-03", "city": "Hays",
                          "post_code": "28635", "phone": "+13366966307", "state": "NC", "street": "1984 Jones Avenue",
                          'is_model': True, 'nickname': 'Cassy'}

    def test_add_info_good(self):
        response = self.client.post(reverse('photo:profile_info_api'), self.user_dict, secure=True)
        self.assertEqual(response.status_code, 200)
        pm = User.objects.all()
        self.assertEqual(len(pm), 1)

    def test_add_info_good_without_model_nickname(self):
        self.user_dict.pop('is_model')
        self.user_dict.pop('nickname')
        response = self.client.post(reverse('photo:profile_info_api'), self.user_dict, secure=True)
        self.assertEqual(response.status_code, 200)
        pm = User.objects.all()
        self.assertEqual(len(pm), 1)

    def test_add_info_bad(self):
        self.user_dict.pop('dob')
        response = self.client.post(reverse('photo:profile_info_api'), self.user_dict, secure=True)
        self.assertEqual(response.status_code, 400)
        pm = User.objects.all()
        self.assertEqual(len(pm), 1)

    def test_update_info(self):
        d = self.user_dict.copy()
        d.pop('first_name')
        d.pop('last_name')
        User.objects.filter(email=self.test_user.email).update(**d)

        pm = User.objects.all()
        self.assertEqual(len(pm), 1)
        self.assertEqual(pm[0].state, 'NC')

        self.user_dict['state'] = 'CA'
        response = self.client.post(reverse('photo:profile_info_api'), self.user_dict, secure=True)
        self.assertEqual(response.status_code, 200)
        pm = User.objects.all()
        self.assertEqual(len(pm), 1)
        self.assertEqual(pm[0].state, 'CA')

    def test_get_profile_info_exists(self):
        d = self.user_dict.copy()
        self.test_user.first_name = d.pop('first_name')
        self.test_user.last_name = d.pop('last_name')
        self.test_user.save()
        User.objects.filter(email=self.test_user.email).update(**d)
        response = self.client.get(reverse('photo:profile_info_api'), secure=True)
        self.assertEqual(response.status_code, 200)
        logging.debug(response.data)

    def test_get_profile_info(self):
        response = self.client.get(reverse('photo:profile_info_api'), secure=True)
        self.assertEqual(response.status_code, 200)
        logging.debug(response.data)