import os
from PIL import Image

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect

# Create your views here.
from django.views import generic, View
from ..models import Gallery, Images
from ..forms import GalleryForm, ImageForm
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class GalleryView(LoginRequiredMixin, View):

    def get(self, request, gallery_id, *args, **kwargs):
        gallery = get_object_or_404(Gallery, pk=gallery_id)
        images = gallery.images_set.all()
        form = ImageForm()
        logging.debug(gallery_id)
        gallery_form = GalleryForm(instance=gallery)
        owner = gallery.owner == request.user
        logging.debug(owner)
        logging.debug(gallery.release.all())
        releases = gallery.release.all()
        models = []
        for release in releases:
            d = {}
            if release.use_full_name:
                d['name'] = release.talent_full_name
                d['links'] = release.talent.links_set.all()
            elif release.use_first_name:
                d['name'] = release.talent_first_name
            elif release.use_nickname:
                d['name'] = release.talent_nickname
            models.append(d)
        # context = self.get_gallery(request, gallery_id)
        d = {'form': form, 'images': images, 'gallery': gallery, 'gallery_form': gallery_form, 'update': True,
             'owner': owner, 'models': models}
        return render(request, 'photo_app/gallery.html', d)
