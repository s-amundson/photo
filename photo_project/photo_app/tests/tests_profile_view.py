import logging

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..models import Images, Gallery, Release, User, ReleaseTemplate

logger = logging.getLogger(__name__)


class TestsProfile(TestCase):
    fixtures = ['f1']

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        self.User = get_user_model()
        self.test_user = self.User.objects.get(email='EmilyNConlan@einrot.com')

    def test_get_no_auth(self):
        response = self.client.get(reverse('photo:profile'), secure=True)
        self.assertEqual(response.status_code, 302)

    def test_get_auth1(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('photo:profile'), secure=True)
        logging.debug(response.context['gallery_list'])
        self.assertEqual(len(response.context['gallery_list']), 3)
        self.assertEqual(len(response.context['release_list']), 1)
        self.assertEqual(response.status_code, 200)

    def test_get_auth2(self):
        self.client.force_login(self.User.objects.get(pk=2))
        r = Release(id=2, compensation=2, file=None, name='name', is_mature=False, photographer=User.objects.get(pk=1),
                    talent=User.objects.get(pk=2), shoot_date="2020-02-02", state='pending',
                    template=ReleaseTemplate.objects.get(pk=1), use_first_name=True, use_nickname=True,
                    talent_first_name='firstname', talent_nickname='nick', talent_full_name='full')
        r.save()

        response = self.client.get(reverse('photo:profile'), secure=True)
        self.assertEqual(len(response.context['gallery_list']), 2)
        self.assertEqual(len(response.context['release_list']), 2)
        self.assertEqual(response.status_code, 200)

