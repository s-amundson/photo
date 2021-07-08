import os
from PIL import Image

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect

# Create your views here.
from django.views import generic, View
from ..models import Gallery, Images
from ..forms import ImageForm
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class GalleryView(LoginRequiredMixin, View):

    def get(self, request, gallery_id, *args, **kwargs):
        gallery = get_object_or_404(Gallery, pk=gallery_id)
        images = gallery.images_set.all()
        form = ImageForm()
        # context = self.get_gallery(request, gallery_id)
        return render(request, 'photo_app/gallery.html', {'form': form, 'images': images, 'gallery': gallery})
