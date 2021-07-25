import os
from PIL import Image
import PIL.ExifTags
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.forms import model_to_dict

# Create your views here.
from django.views import generic, View
from ..models import Gallery, Images
from ..forms import ImageForm
import logging

# Get an instance of a logger
# logger = logging.getLogger(__name__)


class ImageView(LoginRequiredMixin, View):

    def get(self, request, image_id, *args, **kwargs):
        image = get_object_or_404(Images, pk=image_id)
        image_data = model_to_dict(image, exclude=['image'])
        i = Image.open(image.image)

        exif = {
            PIL.ExifTags.TAGS[k]: v
            for k, v in i._getexif().items()
            if k in PIL.ExifTags.TAGS
        }
        del exif['MakerNote']

        return render(request, 'photo_app/image.html', {'image': image, 'image_data': exif})
