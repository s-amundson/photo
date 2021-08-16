from PIL import Image
import PIL.ExifTags
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.utils.datetime_safe import date
from django_sendfile import sendfile

# Create your views here.
from django.views import View
from ..models import Images

class ImageCheckAuth:
    def check_auth(self, image, user):
        if user.is_authenticated:
            if user.is_staff or user.is_superuser:
                return True
            elif image.gallery.owner == user:
                return True
            elif self.talent_is_user(image.gallery, user):
                return True
            elif self.public_gallery(image.gallery):
                return not image.private
        else:
            if self.public_gallery(image.gallery):
                return not image.private

    def talent_is_user(self, gallery, user):
        releases = gallery.release.all()
        for release in releases:
            if release.talent == user:
                return True
        return False

    def public_gallery(self, gallery):
        if not gallery.is_public:
            return False
        else:
            if gallery.public_date is None or gallery.public_date >= date.today():
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


class ImageView(LoginRequiredMixin, View):

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
            else:
                orientation = o
        else:
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

        return render(request, 'photo_app/image.html', {'image': image, 'image_data': image_data})
