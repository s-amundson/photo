import os
import json

from django.conf import settings
from django.test import TestCase, Client, tag
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from ..models import Images, Gallery, Release, Talent
import logging
logger = logging.getLogger(__name__)


class TestsImage(TestCase):
    fixtures = ['f1', 'image']

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        self.User = get_user_model()
        self.test_user = self.User.objects.get(pk=2)
        self.client.force_login(self.test_user)

    # @tag('temp')
    def test_get_image_auth(self):
        self.test_user = self.User.objects.get(pk=1)
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('photo:image', kwargs={'image_id': 1}), secure=True)
        self.assertEqual(response.status_code, 200)

    # @tag('temp')
    def test_get_image_model_auth(self):
        g = Gallery.objects.get(pk=1)
        # g.release.add(Release.objects.get(pk=1))
        g.talent.add(Talent.objects.get(pk=2))
        g.save()
        response = self.client.get(reverse('photo:image', kwargs={'image_id': 1}), secure=True)
        self.assertTemplateUsed('photo_app/image.html')
        self.assertEqual(response.status_code, 200)

    @tag('denied')
    def test_get_image_no_auth(self):
        response = self.client.get(reverse('photo:image', kwargs={'image_id': 1}), secure=True)
        self.assertEqual(response.status_code, 403)

    @tag('denied')
    def test_get_image_model_privacy_photographer(self):
        g = Gallery.objects.get(pk=1)
        g.release.add(Release.objects.get(pk=1))
        g.save()
        i = Images.objects.get(pk=1)
        i.privacy_level = 'photographer'
        i.save()

        response = self.client.get(reverse('photo:image', kwargs={'image_id': 1}), secure=True)
        self.assertTemplateUsed('photo_app/image.html')
        self.assertEqual(response.status_code, 403)

    # @tag('temp')
    def test_get_image_public(self):
        g = Gallery.objects.get(pk=1)
        g.privacy_level = 'public'
        g.save()
        i = Images.objects.get(pk=1)
        i.privacy_level = 'public'
        i.save()
        response = self.client.get(reverse('photo:image', kwargs={'image_id': 1}), secure=True)
        self.assertEqual(response.status_code, 200)

    # @tag('temp')
    def test_get_image_get_public(self):
        g = Gallery.objects.get(pk=1)
        g.privacy_level = 'public'
        g.save()
        i = Images.objects.get(pk=1)
        i.privacy_level = 'public'
        i.save()
        response = self.client.get(reverse('photo:image_get', kwargs={'image_id': 1}), secure=True)
        self.assertEqual(response.status_code, 200)

    # @tag('temp')
    def test_get_image_public_logout(self):
        g = Gallery.objects.get(pk=1)
        g.privacy_level = 'public'
        g.save()
        i = Images.objects.get(pk=1)
        i.privacy_level = 'public'
        i.save()
        self.client.logout()
        response = self.client.get(reverse('photo:image', kwargs={'image_id': 1}), secure=True)
        self.assertEqual(response.status_code, 200)

    # @tag('temp')
    def test_get_add_image(self):
        self.test_user = self.User.objects.get(pk=1)
        self.client.force_login(self.test_user)
        g = Gallery.objects.get(pk=1)
        g.privacy_level = 'public'
        g.save()
        i = Images.objects.get(pk=1)
        i.privacy_level = 'public'
        i.save()
        response = self.client.get(reverse('photo:add_image', kwargs={'gallery_id': 1}), secure=True)
        self.assertEqual(response.status_code, 200)

    # @tag('temp')
    def test_get_image_publicdate_future(self):
        g = Gallery.objects.get(pk=1)
        g.privacy_level = 'public'
        g.public_date = timezone.now() + timezone.timedelta(days=3)
        g.save()
        i = Images.objects.get(pk=1)
        i.privacy_level = 'public'
        i.save()
        self.client.logout()
        response = self.client.get(reverse('photo:image', kwargs={'image_id': 1}), secure=True)
        self.assertEqual(response.status_code, 302)

    # @tag('temp')
    def test_get_thumb_auth(self):
        self.test_user = self.User.objects.get(pk=1)
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('photo:thumb', kwargs={'image_id': 1}), secure=True)
        self.assertEqual(response.status_code, 200)

    # @tag('temp')
    def test_get_thumb_no_auth(self):
        response = self.client.get(reverse('photo:thumb', kwargs={'image_id': 1}), secure=True)
        self.assertEqual(response.status_code, 403)

    # @tag('temp')
    def test_post_add_image(self):
        self.test_user = self.User.objects.get(pk=1)
        self.client.force_login(self.test_user)
        g = Gallery(privacy_level='private', name='test', owner=self.test_user,
                    public_date=None, shoot_date='2021-06-26')
        g.save()
        g.release.add(Release.objects.get(pk=1))

        p = os.path.join(settings.BASE_DIR, 'photo_app', 'media', '1.jpg')
        with open(p, 'rb') as f:
            response = self.client.post(reverse('photo:add_image', kwargs={'gallery_id': 1}),
                                        {'image': f, 'gallery': g.id, 'privacy_level': 'private'}, secure=True)

        response = self.client.get(reverse('photo:image', kwargs={'image_id': 1}), secure=True)
        self.assertEqual(response.status_code, 200)

    # @tag('temp')
    def test_carousel_add(self):
        response = self.client.post(reverse('photo:image_carousel', kwargs={'pk': 1}), {'carousel': True}, secure=True)
        self.assertEqual(response.status_code, 200)
        i = Images.objects.get(pk=1)
        self.assertTrue(i.carousel)
        content = json.loads(response.content)
        self.assertEqual(content['status'], 'success')
        self.assertTrue(content['carousel'])

    @tag('temp')
    def test_carousel_remove(self):
        i = Images.objects.get(pk=1)
        i.carousel = True
        i.save()

        response = self.client.post(reverse('photo:image_carousel', kwargs={'pk': 1}), {'carousel': False}, secure=True)
        self.assertEqual(response.status_code, 200)
        i = Images.objects.get(pk=1)
        self.assertFalse(i.carousel)
        content = json.loads(response.content)
        self.assertEqual(content['status'], 'success')
        self.assertFalse(content['carousel'])
