import logging
import os

from PIL import Image
from django.conf import settings
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from ..models import Images, Gallery

logger = logging.getLogger(__name__)


class TestsImage(TestCase):
    fixtures = ['f1']

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        self.User = get_user_model()
        self.test_user = self.User.objects.get(pk=1)
        # self.test_user = User.objects.create_user(username='fred', password='secret')
        self.client.force_login(self.test_user)


    def test_post_image(self):
        g = Gallery(is_public=False, name='test', owner=self.test_user,
                    public_date=None, shoot_date='2021-06-26')
        g.save()
        g.photo_model.add(self.User.objects.get(pk=2))

        # pic = SimpleUploadedFile("1.jpg", "file_content", content_type="video/mp4")
        # with open() as f:
        p = os.path.join(settings.BASE_DIR, 'photo_app', 'fixtures', '1.jpg')
        with open(p, 'rb') as f:
            response = self.client.post(reverse('photo:image_upload', kwargs={'gallery_id': 1}),
                                        {'image': f, 'gallery': g.id}, secure=True)

        self.assertEqual(response.status_code, 200)
