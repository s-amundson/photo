import logging
import os

from django.conf import settings
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile

from ..models import Images, Gallery, Release, User, ReleaseTemplate

logger = logging.getLogger(__name__)


class TestsModelRelease(TestCase):
    fixtures = ['f1']

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        self.User = get_user_model()
        self.test_user = self.User.objects.get(pk=1)
        self.release_dict = {'compensation': 2,
                             # 'file': None,
                             'name': 'name',
                             'is_mature': False,
                             'photographer': 1,
                             'talent': 2,
                             'shoot_date': "2020-02-02",
                             # 'state': 'pending',
                             'template': 1,
                             'use_first_name': True,
                             'use_nickname': True }
        self.release_dict_model_info = {'model_first_name': 'firstname',
                                        'model_nickname': 'nick',
                                        'model_full_name': 'full'}
        self.img = 'data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoDhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCAC2AX4DASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD6pooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigD//Z',


    def test_get_noauth_start(self):
        response = self.client.get(reverse('photo:model_release'), secure=True)
        self.assertEqual(response.status_code, 302)

    def test_get_not_photographer_start(self):
        self.client.force_login(self.User.objects.get(pk=2))
        response = self.client.get(reverse('photo:model_release'), secure=True)
        self.assertEqual(response.status_code, 404)

    def test_get_photographer_start(self):
        self.client.force_login(self.test_user) # this user is photographer
        response = self.client.get(reverse('photo:model_release'), secure=True)
        self.assertEqual(response.status_code, 200)

    def test_get_photographer_return(self):
        r = Release(id=1, compensation=2, file=None, name='name', is_mature=False, photographer=User.objects.get(pk=1),
                    talent=User.objects.get(pk=2), shoot_date="2020-02-02", state='pending',
                    template=ReleaseTemplate.objects.get(pk=1), use_first_name=True, use_nickname=True,
                    talent_first_name='firstname', talent_nickname='nick', talent_full_name='full')
        r.save()
        self.client.force_login(self.test_user)  # this user is photographer
        response = self.client.get(reverse('photo:model_release', kwargs={'release': r.id}), secure=True)
        self.assertEqual(response.status_code, 200)

    def test_get_photographer_return_complete(self):
        r = Release(id=1, compensation=2, file=None, name='name', is_mature=False, photographer=User.objects.get(pk=1),
                    talent=User.objects.get(pk=2), shoot_date="2020-02-02", state='complete',
                    template=ReleaseTemplate.objects.get(pk=1), use_first_name=True, use_nickname=True,
                    talent_first_name='firstname', talent_nickname='nick', talent_full_name='full')
        r.save()
        self.client.force_login(self.test_user)  # this user is photographer
        response = self.client.get(reverse('photo:model_release', kwargs={'release': r.id}), secure=True)
        self.assertEqual(response.status_code, 200)

    def test_get_as_model(self):
        self.client.force_login(self.User.objects.get(pk=2))
        r = Release(id=1, compensation=2, file=None, name='name', is_mature=False, photographer=User.objects.get(pk=1),
                    talent=User.objects.get(pk=2), shoot_date="2020-02-02", state='pending',
                    template=ReleaseTemplate.objects.get(pk=1), use_first_name=True, use_nickname=True,
                    talent_first_name='firstname', talent_nickname='nick', talent_full_name='full')
        r.save()

        response = self.client.get(reverse('photo:model_release', kwargs={'release': r.id}), secure=True)
        # self.assertEqual(len(response.context['gallery_list']), 2)
        # self.assertEqual(len(response.context['release_list']), 1)
        self.assertEqual(response.status_code, 200)

    def test_get_as_different_model(self):
        self.client.force_login(self.User.objects.get(pk=3))
        r = Release(id=1, compensation=2, file=None, name='name', is_mature=False, photographer=User.objects.get(pk=1),
                    talent=User.objects.get(pk=2), shoot_date="2020-02-02", state='pending',
                    template=ReleaseTemplate.objects.get(pk=1), use_first_name=True, use_nickname=True,
                    talent_first_name='firstname', talent_nickname='nick', talent_full_name='full')
        r.save()

        response = self.client.get(reverse('photo:model_release', kwargs={'release': r.id}), secure=True)
        self.assertEqual(response.status_code, 403)

    def test_post_photographer_start(self):
        self.client.force_login(self.test_user) # this user is photographer
        response = self.client.post(reverse('photo:model_release'), self.release_dict, secure=True)
        ml = Release.objects.all()
        self.assertEqual(len(ml), 2)
        ml = ml[1]
        self.assertEqual(ml.state, 'started')
        self.assertRedirects(response, reverse('photo:index'))

    def test_post_photographer_start_error(self):
        self.client.force_login(self.test_user) # this user is photographer
        # set an invalid date
        self.release_dict['shoot_date'] = '13/15/23'
        response = self.client.post(reverse('photo:model_release'), self.release_dict, secure=True)
        self.assertEqual(response.status_code, 200)
        ml = Release.objects.all()
        self.assertEqual(len(ml), 1)

    def test_post_photographer_update(self):
        r = Release(id=2, compensation=2, file=None, name='name', is_mature=False, photographer=User.objects.get(pk=1),
                    talent=User.objects.get(pk=2), shoot_date="2020-02-02", state='pending',
                    template=ReleaseTemplate.objects.get(pk=1), use_first_name=True, use_nickname=True,
                    talent_first_name='firstname', talent_nickname='nick', talent_full_name='full')
        r.save()
        logging.debug(r.id)
        self.release_dict['shoot_date'] = '2020-04-04'
        # self.release_dict['photographer_signature'] = self.img
        self.client.force_login(self.test_user) # this user is photographer

        response = self.client.post(reverse('photo:model_release', kwargs={'release': r.id}), self.release_dict,
                                    secure=True)
        self.assertRedirects(response, reverse('photo:index'))
        ml = Release.objects.all()
        self.assertEqual(len(ml), 2)
        ml = ml[1]
        self.assertEqual(ml.state, 'pending')
        self.assertEqual(ml.shoot_date.month, 4)

    def test_post_model_pending(self):
        user = self.User.objects.get(pk=2)
        self.client.force_login(user)
        r = Release(compensation=2, name='name', is_mature=False, photographer=User.objects.get(pk=1),
                    talent=User.objects.get(pk=2), shoot_date="2020-02-02", state='pending',
                    template=ReleaseTemplate.objects.get(pk=1), use_first_name=True, use_nickname=True)
        r.save()
        d = {'use_first_name': False, 'use_full_name': False, 'use_nickname': True, 'talent_signature': self.img,
             'template': 1}
        response = self.client.post(reverse('photo:model_release', kwargs={'release': r.id}), d, secure=True)
        self.assertRedirects(response, reverse('photo:index'))
        ml = Release.objects.all()
        self.assertEqual(len(ml), 2)
        ml = ml[1]
        self.assertEqual(ml.state, 'agreed')
        self.assertFalse(ml.use_first_name)
        self.assertFalse(ml.use_full_name)
        self.assertEqual(ml.talent_first_name, user.first_name)

    def test_post_model_update(self):
        user = self.User.objects.get(pk=2)
        self.client.force_login(user)
        r = Release(compensation=2, name='name', is_mature=False, photographer=User.objects.get(pk=1),
                    talent=User.objects.get(pk=2), shoot_date="2020-02-02", state='pending',
                    template=ReleaseTemplate.objects.get(pk=1), use_first_name=True, use_nickname=True)
        r.save()
        d = {'use_first_name': False, 'use_full_name': False, 'use_nickname': True, 'template': 1}
        response = self.client.post(reverse('photo:model_release_update', kwargs={'release': r.id}), d, secure=True)
        ml = Release.objects.all()
        self.assertEqual(len(ml), 2)
        ml = ml[1]
        self.assertEqual(ml.state, 'pending')
        self.assertFalse(ml.use_first_name)
        self.assertFalse(ml.use_full_name)
        self.assertEqual(ml.talent_first_name, None)

    def test_post_different_model_pending(self):
        user = self.User.objects.get(pk=3)
        self.client.force_login(user)
        r = Release(compensation=2, name='name', is_mature=False, photographer=User.objects.get(pk=1),
                    talent=User.objects.get(pk=2), shoot_date="2020-02-02", state='pending',
                    template=ReleaseTemplate.objects.get(pk=1), use_first_name=True, use_nickname=True)
        r.save()
        d = {'use_first_name': False, 'use_full_name': False, 'use_nickname': True, 'agree': True, 'template': 1}
        response = self.client.post(reverse('photo:model_release', kwargs={'release': r.id}), d, secure=True)
        self.assertEqual(response.status_code, 403)
        ml = Release.objects.all()
        self.assertEqual(len(ml), 2)
        ml = ml[1]
        self.assertEqual(ml.state, 'pending')

    def test_post_photographer_agreed(self):
        self.client.force_login(self.test_user)  # this user is photographer
        p = os.path.join(settings.BASE_DIR, 'photo_app', 'fixtures', '1.jpg')
        r = Release(compensation=2, name='name', is_mature=False, photographer=User.objects.get(pk=1),
                    talent=User.objects.get(pk=2), shoot_date="2020-02-02", state='started',
                    template=ReleaseTemplate.objects.get(pk=1), use_first_name=True, use_nickname=True)
        # r.talent_signature = SimpleUploadedFile(name='test_image.jpg', content=open(p, 'rb').read(),
        #                                         content_type='image/jpeg')
        r.save()

        self.release_dict['photographer_signature'] = self.img
        response = self.client.post(reverse('photo:model_release', kwargs={'release': r.id}), self.release_dict, secure=True)
        self.assertEqual(response.status_code, 302)
        ml = Release.objects.all()
        self.assertEqual(len(ml), 2)
        ml = ml[1]
        self.assertNotEquals(ml.file, None)
        self.assertEqual(ml.state, 'pending')

