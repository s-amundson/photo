import logging

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..models import Release, User, ReleaseTemplate

logger = logging.getLogger(__name__)


class TestsReleaseTemplate(TestCase):
    fixtures = ['f1']

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        self.User = get_user_model()
        # self.test_user = self.User.objects.get(pk=1)

        self.test_dict = {'description': 'shoot', 'name': 'test shoot', 'photo_model': 2, 'shoot_date': '2020-02-02',
                          'template': 1, 'compensation': '$$$$', 'is_mature': 'false', 'use_first_name': 'true',
                          'use_full_name': 'true', 'use_nickname': 'true'}

    def test_get_auth1(self):
        self.client.force_login(self.User.objects.get(pk=1))
        response = self.client.get(reverse('photo:release_preview', kwargs={'template': 1}), secure=True)
        self.assertTrue(response.context['use_full_name'])
        # self.assertEqual(len(response.context['release_list']), 1)
        self.assertEqual(response.status_code, 200)

    def test_get_auth2(self):
        self.client.force_login(self.User.objects.get(pk=2))
        s = self.client.session
        s['model_release'] = 2
        s.save()
        r = Release(id=2, compensation=2, file=None, name='name', is_mature=False, photographer=User.objects.get(pk=1),
                    talent=User.objects.get(pk=2), shoot_date="2020-02-02", state='pending',
                    template=ReleaseTemplate.objects.get(pk=1), use_first_name=True, use_nickname=True,
                    talent_first_name='firstname', talent_nickname='nick', talent_full_name='full')
        r.save()
        response = self.client.get(reverse('photo:release_preview', kwargs={'template': 1}), secure=True)
        logging.debug(response.context)
        self.assertTrue(response.context['use_full_name'])
        self.assertEqual(response.context['talent']['first_name'], 'Rosalva')
        # self.assertEqual(len(response.context['release_list']), 1)
        self.assertEqual(response.status_code, 200)

    def test_get_no_auth1(self):
        self.client.force_login(self.User.objects.get(pk=2))
        s = self.client.session
        s['model_release'] = None
        s.save()
        # response = self.client.get(reverse('photo:release_preview', kwargs={'template': 1}), secure=True)
        response = self.client.get('/release_preview/1/', secure=True)
        # self.assertTrue(response.context['use_full_name'])
        # self.assertEqual(len(response.context['release_list']), 1)
        self.assertEqual(response.status_code, 405)

    def test_post_new(self):
        self.client.force_login(self.User.objects.get(pk=1))

        response = self.client.post(reverse('photo:release_preview', kwargs={'template': 1}), self.test_dict,
                                    secure=True)
        logging.debug(response.context)
        self.assertTrue(response.context['use_full_name'])
        self.assertEqual(response.status_code, 200)

    def test_post_talent(self):
        self.client.force_login(self.User.objects.get(pk=2))
        s = self.client.session
        s['model_release'] = 2
        s.save()
        r = Release(id=2, compensation=2, file=None, name='name', is_mature=False, photographer=User.objects.get(pk=1),
                    talent=User.objects.get(pk=2), shoot_date="2020-02-02", state='pending',
                    template=ReleaseTemplate.objects.get(pk=1), use_first_name=True, use_nickname=True,
                    talent_first_name='firstname', talent_nickname='nick', talent_full_name='full')
        r.save()
        response = self.client.post(reverse('photo:release_preview', kwargs={'template': 1}), self.test_dict,
                                    secure=True)
        logging.debug(response.context)
        self.assertTrue(response.context['use_full_name'])
        self.assertEqual(response.status_code, 200)

