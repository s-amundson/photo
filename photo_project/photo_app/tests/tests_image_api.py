import logging
import os

from PIL import Image
from django.conf import settings
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..models import Images, Gallery

logger = logging.getLogger(__name__)


class TestsImage(TestCase):
    # fixtures = ['f1']

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        User = get_user_model()
        # self.test_user = User.objects.get(username='EmilyNConlan@einrot.com')
        self.test_user = User.objects.create_user(username='fred', password='secret')
        self.client.force_login(self.test_user)


    def test_post_image(self):
        g = Gallery(is_public=False, name='test', owner=self.test_user, photo_model=None,
                    public_date=None, shoot_date='2021-06-26')
        # with open() as f:
        p = os.path.join(settings.BASE_DIR, 'photo_app', 'fixtures', '1.jpeg')
        # p = "/home/sam/PycharmProjects/photo/photo_project/photo_app/static/images/target2.png"
        logging.debug(p)
        img = Image.open(p)

        response = self.client.post(reverse('photo:image_upload'), {'image': img, 'gallery': g}, secure=True)
        self.assertEqual(response.status_code, 200)

    # def test_costs_get_page(self):
    #     # Change user then Get the page
    #     response = self.client.get(reverse('registration:costs'), secure=True)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed('student_app/costs.html')