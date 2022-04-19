from PIL import Image
import PIL.ExifTags
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.utils.datetime_safe import date, datetime
from django_sendfile import sendfile

# Create your views here.
from django.views import View
from ..forms import ImageForm, ImageUpdateForm
from ..models import Gallery, Images
from ..src import Img

# Get an instance of a logger
import logging
logger = logging.getLogger(__name__)


class AddImageView(UserPassesTestMixin, FormView):
    form_class = ImageForm
    gallery = None
    image = None
    template_name = 'photo_app/form_as_p.html'
    success_url = reverse_lazy('photo:index')

    def form_invalid(self, form):
        logging.info(form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):
        logging.info(form.cleaned_data)
        if form.cleaned_data['image'] is not None:
            record = form.save(commit=False)
            record.gallery = self.gallery
            img = Img(record.image)
            img.update_record(record)
        else:
            form.save()

        return super().form_valid(form)


    def test_func(self):
        if self.request.user.is_authenticated:
            gid = self.kwargs.get('gallery_id', None)
            iid = self.kwargs.get('image_id', None)
            if gid is not None:
                self.gallery = get_object_or_404(Gallery, pk=gid)
                if iid is not None:
                    self.image = get_object_or_404(Images, pk=iid)
                    self.success_url = reverse_lazy('photo:image', kwargs={'image_id': iid})
                else:
                    self.success_url = reverse_lazy('photo:gallery_view', kwargs={'gallery_id': gid})
            return self.request.user.is_staff
        else:
            return False


class ImageCheckAuth:
    def check_auth(self, image, user):
        logging.debug(user.is_authenticated)
        if user.is_authenticated:
            logging.debug(image.privacy_level)
            logging.debug(self.public_gallery(image.gallery))
            if user.is_staff or user.is_superuser:
                return True
            elif image.gallery.owner == user:  # pragma: no cover
                return True
            elif self.talent_is_user(image.gallery, user):
                return image.privacy_level in ['private', 'public']
            elif self.public_gallery(image.gallery):
                return image.privacy_level == 'public'
        else:
            if self.public_gallery(image.gallery):
                return image.privacy_level == 'public'

    def talent_is_user(self, gallery, user):
        releases = gallery.release.all()
        for release in releases:
            if release.talent == user:
                return True
        return False

    def public_gallery(self, gallery):
        if not gallery.privacy_level == 'public':
            return False
        else:
            if gallery.public_date is None or gallery.public_date <= date.today():
                return True
            else:
                return False


class ImageGetView(View):
    def get(self, request, image_id, thumb=False):
        image = get_object_or_404(Images, pk=image_id)

        if ImageCheckAuth().check_auth(image, request.user):
            if thumb:
                return sendfile(request, image.thumb.path)
            return sendfile(request, image.image.path)

        return HttpResponseForbidden()


class ImageGetThumbView(ImageGetView):
    def get(self, request, image_id):
        return super().get(request, image_id, thumb=True)


class ImageView(View):

    def get(self, request, image_id, *args, **kwargs):
        image = get_object_or_404(Images, pk=image_id)
        if not ImageCheckAuth().check_auth(image, request.user):
            return HttpResponseForbidden()
        # image_data = model_to_dict(image, exclude=['image'])
        i = Image.open(image.image)
        edata = i._getexif()
        if edata is not None:
            exif = {
                PIL.ExifTags.TAGS[k]: v
                for k, v in i._getexif().items()
                if k in PIL.ExifTags.TAGS
            }
            del exif['MakerNote']
            o = exif.get('Orientation', '')
            if o == 1 or o == 3:
                orientation = "Landscape"
            elif o == 8 or o == 6:
                orientation = "Portrait"
            else:  # pragma: no cover
                orientation = o
        else:  # pragma: no cover
            exif = {}
            orientation = ''
        image_data = {'Camera': exif.get('Model', ''),
                      'Orientation': orientation,
                      'Taken': exif.get('DateTimeOriginal', ''),
                      'ExposureTime': exif.get('ExposureTime', ''),
                      'F-Stop': exif.get('FNumber', ''),
                      'ISO': exif.get('ISOSpeedRatings', ''),
                      'Focal Length': exif.get('FocalLength', ''),
                      'Film Focal Length': exif.get('FocalLengthIn35mmFilm', ''),
                      'Height': exif.get('ExifImageHeight',''),
                      'Width': exif.get('ExifImageWidth', ''),
                      'Filename': image.image.name.split('/')[-1]
                      }
        form = ImageForm(instance=image)
        return render(request, 'photo_app/image.html', {'image': image, 'image_data': image_data, 'form': form})


class UpdateImageView(AddImageView):
    form_class = ImageUpdateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.image
        return kwargs

    def test_func(self):
        if self.request.user.is_authenticated:
            iid = self.kwargs.get('image_id', None)
            if iid is not None:
                self.image = get_object_or_404(Images, pk=iid)
                self.gallery = self.image.gallery
                self.success_url = reverse_lazy('photo:image', kwargs={'image_id': iid})
            return self.request.user.is_staff
        else:
            return False
