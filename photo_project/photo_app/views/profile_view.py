from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.views.generic.base import View

import logging

from ..forms import LinkForm
from ..models import Gallery, Links, Release
logger = logging.getLogger(__name__)


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        logging.debug(request.user)
        gallery_list = []
        try:
            gl = Gallery.objects.filter(Q(release__talent=request.user) | Q(owner=request.user) |
                                                  Q(photographer=request.user))
            for g in gl:
                if g not in gallery_list:
                    gallery_list.append(g)
        except Gallery.DoesNotExist:  # pragma: no cover
            pass
        release_list = []
        rl = Release.objects.filter(Q(talent=request.user) | Q(photographer=request.user))
        for r in rl:
            if r not in release_list:
                release_list.append(r)

        logging.debug(release_list)

        links = Links.objects.filter(user=request.user)
        link_form = LinkForm()

        # form = PhotoModelForm(initial=pm)
        return render(request, 'photo_app/profile.html', {'gallery_list': gallery_list, 'release_list': release_list,
                      'links': links, 'form': link_form})
