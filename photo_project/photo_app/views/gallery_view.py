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
        return render(request, 'photo_app/gallery.html', {'form': form, 'images': images})

    def get_gallery(self, request, gallery_id, image_size=0):
        logging.warning(request.user.id)
        try:
            gallery = Gallery.objects.filter(pk=gallery_id, owner=request.user.id)[0]
        except IndexError:
            return redirect('index/')

        if len(child_galleries) == 0:
            child_galleries = None
        logger.warning(child_galleries)
        gallery_path = gallery.directory
        parent = gallery.parent
        while parent > 0:
            logging.warning(parent)
            try:
                g = Gallery.objects.get(pk=parent)
                gallery_path = os.path.join(g.directory, gallery_path)
                parent = g.parent
            except Gallery.DoesNotExist:
                parent = 0
        gallery_path = os.path.join(settings.GALLERY_DIR, gallery_path)
        logging.warning(image_size)
        images = gallery.images_set.filter(width__gte=image_size) | gallery.images_set.filter(height__gte=image_size)

        form = ImageForm()
        return {'form': form, 'images': images, 'gallery_path': gallery_path, 'child_galleries': child_galleries,
                   'gallery': gallery}


    def post(self, request):
        logger.warning(request.POST)
        logger.warning(request.POST.get('image_size'))
        logger.warning(type(request.POST.get('image_size')))
        logger.warning(int(request.POST.get('image_size')))
        context = self.get_gallery(request, int(request.POST.get('gallery')[0]),
                                   int(request.POST.get('image_size')))
        return render(request, 'gallery_app/gallery.html', context)