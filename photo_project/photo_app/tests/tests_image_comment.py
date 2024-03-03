
from django.test import TestCase, Client, tag
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..models import ImageComment
import logging
logger = logging.getLogger(__name__)


class TestsImageComment(TestCase):
    fixtures = ['f1', 'image', 'image_comment']

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        self.User = get_user_model()
        self.post_data = {"comment":  "test_comment",
                          "comment_date": "2022-01-06T16:33:56.868Z",
                          "image":  1,
                          "privacy_level":  "private",
                          "user": 1}

    # @tag('temp')
    def test_get_image_comments_staff(self):
        self.test_user = self.User.objects.get(pk=1)
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('photo:image_comment', kwargs={'image_id': 1}), secure=True)
        self.assertEqual(len(response.context['comments']), 3)
        self.assertEqual(response.status_code, 200)

    # @tag('temp')
    def test_get_image_comments_auth_self(self):
        self.test_user = self.User.objects.get(pk=2)
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('photo:image_comment', kwargs={'image_id': 1}), secure=True)
        self.assertEqual(len(response.context['comments']), 1)
        self.assertEqual(response.status_code, 200)

    # @tag('temp')
    def test_get_image_comments_auth_public(self):
        self.test_user = self.User.objects.get(pk=3)
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('photo:image_comment', kwargs={'image_id': 1}), secure=True)
        self.assertEqual(len(response.context['comments']), 2)
        self.assertEqual(response.status_code, 200)

    # @tag('temp')
    def test_get_image_no_auth(self):
        response = self.client.get(reverse('photo:image_comment', kwargs={'image_id': 1}), secure=True)
        self.assertEqual(response.status_code, 302)

    # @tag('temp')
    def test_post_image_comment_auth(self):
        self.test_user = self.User.objects.get(pk=3)
        self.client.force_login(self.test_user)
        self.post_data['user'] = 3
        response = self.client.post(reverse('photo:image_comment', kwargs={'image_id': 1}), self.post_data, secure=True)
        self.assertEqual(response.status_code, 302)
        ic = ImageComment.objects.all()
        self.assertEqual(len(ic), 4)
