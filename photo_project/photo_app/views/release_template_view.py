from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404, render

from django.views import View
from ..models import Release

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class ReleaseTemplateView(UserPassesTestMixin, View):
    release = None

    def get(self, request, release_id):
        return render(request, f'photo_app/release/{self.release.template.file}.html', {'release': self.release})

    def test_func(self):
        if self.request.user.is_authenticated:
            release_id = self.kwargs.get('release_id', None)
            logging.debug(release_id)
            if release_id is None:
                return False
            self.release = get_object_or_404(Release, pk=release_id)
            if self.request.user.is_staff:
                return True
            if self.request.user == self.release.photographer or self.request.user == self.release.talent:
                return True
            return False
