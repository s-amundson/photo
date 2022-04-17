import os

from django.conf import settings
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from ..models import Images, Gallery, Release
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

    def test_get_image_auth(self):
        self.test_user = self.User.objects.get(pk=1)
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('photo:image', kwargs={'image_id': 1}), secure=True)
        self.assertEqual(response.status_code, 200)

    def test_get_image_model_auth(self):
        g = Gallery.objects.get(pk=1)
        g.release.add(Release.objects.get(pk=1))
        g.save()
        response = self.client.get(reverse('photo:image', kwargs={'image_id': 1}), secure=True)
        self.assertTemplateUsed('photo_app/image.html')
        self.assertEqual(response.status_code, 200)

    def test_get_image_no_auth(self):
        response = self.client.get(reverse('photo:image', kwargs={'image_id': 1}), secure=True)
        self.assertEqual(response.status_code, 403)

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

    def test_get_image_public(self):
        g = Gallery.objects.get(pk=1)
        g.privacy_level = 'public'
        g.save()
        i = Images.objects.get(pk=1)
        i.privacy_level = 'public'
        i.save()
        response = self.client.get(reverse('photo:image', kwargs={'image_id': 1}), secure=True)
        self.assertEqual(response.status_code, 200)

    def test_get_image_get_public(self):
        g = Gallery.objects.get(pk=1)
        g.privacy_level = 'public'
        g.save()
        i = Images.objects.get(pk=1)
        i.privacy_level = 'public'
        i.save()
        response = self.client.get(reverse('photo:image_get', kwargs={'image_id': 1}), secure=True)
        self.assertEqual(response.status_code, 200)

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
        self.assertEqual(response.status_code, 403)

    def test_get_thumb_auth(self):
        self.test_user = self.User.objects.get(pk=1)
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('photo:thumb', kwargs={'image_id': 1}), secure=True)
        self.assertEqual(response.status_code, 200)

    def test_get_thumb_no_auth(self):
        response = self.client.get(reverse('photo:thumb', kwargs={'image_id': 1}), secure=True)
        self.assertEqual(response.status_code, 403)

    def test_post_add_image(self):
        self.test_user = self.User.objects.get(pk=1)
        self.client.force_login(self.test_user)
        g = Gallery(privacy_level='private', name='test', owner=self.test_user,
                    public_date=None, shoot_date='2021-06-26')
        g.save()
        g.release.add(Release.objects.get(pk=1))

        # pic = SimpleUploadedFile("1.jpg", "file_content", content_type="video/mp4")
        # with open() as f:
        p = os.path.join(settings.BASE_DIR, 'photo_app', 'media', '1.jpg')
        with open(p, 'rb') as f:
            response = self.client.post(reverse('photo:add_image', kwargs={'gallery_id': 1}),
                                        {'image': f, 'gallery': g.id, 'privacy_level': 'private'}, secure=True)

        response = self.client.get(reverse('photo:image', kwargs={'image_id': 1}), secure=True)
        self.assertEqual(response.status_code, 200)

class TestsImageApi(TestCase):
    fixtures = ['f1']

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        self.User = get_user_model()
        self.test_user = self.User.objects.get(pk=1)
        # self.test_user = User.objects.create_user(username='fred', password='secret')
        self.client.force_login(self.test_user)

    def test_post_image(self):
        g = Gallery(privacy_level='private', name='test', owner=self.test_user,
                    public_date=None, shoot_date='2021-06-26')
        g.save()
        g.release.add(Release.objects.get(pk=1))

        # pic = SimpleUploadedFile("1.jpg", "file_content", content_type="video/mp4")
        # with open() as f:
        p = os.path.join(settings.BASE_DIR, 'photo_app', 'media', '1.jpg')
        with open(p, 'rb') as f:
            response = self.client.post(reverse('photo:image_upload', kwargs={'gallery_id': 1}),
                                        {'image': f, 'gallery': g.id}, secure=True)

        response = self.client.get(reverse('photo:image', kwargs={'image_id': 1}), secure=True)
        self.assertEqual(response.status_code, 200)

    def test_post_image_error(self):
        p = os.path.join(settings.BASE_DIR, 'photo_app', 'media', '1.jpg')
        with open(p, 'rb') as f:
            response = self.client.post(reverse('photo:image_upload', kwargs={'gallery_id': 1}),
                                        {'image': f, 'gallery': 10}, secure=True)

        response = self.client.get(reverse('photo:image', kwargs={'image_id': 1}), secure=True)
        self.assertEqual(response.status_code, 404)