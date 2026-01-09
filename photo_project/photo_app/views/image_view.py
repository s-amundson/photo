from PIL import Image
import PIL.ExifTags
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, UpdateView
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
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
        logging.warning(self.request.POST)
        logging.info(form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):
        image_files = self.request.FILES.getlist('image')
        logging.warning(image_files)
        logging.warning(self.image)
        logging.warning(form.cleaned_data['image'])
        if image_files and form.cleaned_data['image'] is not None:
            for image in image_files:
                img = Img(image)
                record = Images.objects.create(
                    camera_make=img.camera_make,
                    camera_model=img.camera_model,
                    gallery=self.gallery,
                    filename=image.name,
                    image=image,
                    orientation=img.orientation,
                    privacy_level=form.cleaned_data['privacy_level'],
                    # tags = models.CharField(max_length=255)
                    taken=img.taken,
                    thumb=img.img_file,
                    thumb_width=200,
                    width=img.width,
                    height=img.height
                )
        elif form.cleaned_data['image'] is not None:
            img = Img(form.cleaned_data['image'])
            record = form.save(commit=False)
            record.gallery = self.gallery
            record.image = form.cleaned_data['image']
            record.privacy_level = form.cleaned_data['privacy_level']
            img.update_record(record)
        else:
            record = form.save()
            record.privacy_level = form.cleaned_data['privacy_level']
            record.save()

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


class ImageCarouselView(UpdateView):
    model = Images
    fields = ["carousel"]
    template_name = 'photo_app/form_as_p.html'

    def form_invalid(self, form):
        logger.warning(form.errors)
        return JsonResponse({'status': 'error', 'carousel': self.object.carousel})

    def form_valid(self, form):
        logger.warning(self.request.POST)
        logger.warning(form.cleaned_data)
        """If the form is valid, save the associated model."""
        self.object = form.save()
        return JsonResponse({'status': 'success', 'carousel': self.object.carousel})

class ImageCheckAuth:
    def check_auth(self, image, user):
        if user.is_authenticated:
            if user.is_staff or user.is_superuser:
                return True
            elif image.gallery.owner == user:  # pragma: no cover
                return True
            elif self.talent_is_user(image.gallery, user):
                return image.privacy_level in ['private', 'public']
            elif image.gallery.privacy_level == 'authenticated':
                return image.privacy_level in ['public']
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
            if gallery.public_date is None or gallery.public_date <= timezone.now().date():
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


class ImageView(UserPassesTestMixin, FormView):
    form_class = ImageUpdateForm
    model = Images
    template_name = 'photo_app/image.html'
    image = None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.image
        return kwargs

    def get_image_data(self):
        i = Image.open(self.image.image)
        edata = i._getexif()
        # logger.warning(edata)
        if edata is not None:
            exif = {
                PIL.ExifTags.TAGS[k]: v
                for k, v in i._getexif().items()
                if k in PIL.ExifTags.TAGS
            }
            if 'MakerNote' in exif:
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
        return {'Camera': exif.get('Model', ''),
                      'Orientation': orientation,
                      'Taken': exif.get('DateTimeOriginal', ''),
                      'ExposureTime': exif.get('ExposureTime', ''),
                      'F-Stop': exif.get('FNumber', ''),
                      'ISO': exif.get('ISOSpeedRatings', ''),
                      'Focal Length': exif.get('FocalLength', ''),
                      'Film Focal Length': exif.get('FocalLengthIn35mmFilm', ''),
                      'Height': exif.get('ExifImageHeight',''),
                      'Width': exif.get('ExifImageWidth', ''),
                      'Filename': self.image.image.name.split('/')[-1]
                }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logger.warning(context)
        images = self.image.gallery.images_set.filter(privacy_level='public')
        if self.request.user.is_authenticated:
            if self.request.user.is_staff or self.request.user.is_superuser:
                images = self.image.gallery.images_set.all()
            # elif ImageCheckAuth().talent_is_user(image.gallery, request.user):
            elif self.image.gallery.talent.filter(user=self.request.user).count():
                images = self.image.gallery.images_set.filter(privacy_level__in=['public', 'private'])

        images = images.order_by('id')
        prev_image = None
        next_image = None
        img_list = list(images)
        for i in range(len(img_list)):
            if img_list[i] == self.image:
                if i > 0:
                    prev_image = img_list[i-1]
                if i < len(img_list) - 1:
                    next_image = img_list[i+1]

        context["image"] = self.image
        context['prev_image'] = prev_image
        context['next_image'] = next_image
        context['image_data'] = self.get_image_data()
        return context

    def test_func(self):
        logger.warning(self.kwargs.get('image_id'))
        self.image = get_object_or_404(Images, pk=self.kwargs.get('image_id'))
        logger.warning(self.image)
        if self.image.gallery.privacy_level == 'public' and self.image.privacy_level == 'public':
            if self.image.gallery.public_date and self.image.gallery.public_date > timezone.now().date():
                return False
            return True
        if self.request.user.is_authenticated:
            if self.image.privacy_level == 'public' and self.image.gallery.privacy_level in ['authenticated']:
                if self.image.gallery.public_date and self.image.gallery.public_date > timezone.now():
                    return False
                return True
            else:  # gallery is private
                if (self.request.user == self.image.gallery.owner
                        or self.request.user in self.image.gallery.photographer.all()
                        or self.image.gallery.talent.filter(user=self.request.user).count()):
                    return True
        return False


class UpdateImageView(AddImageView):
    form_class = ImageUpdateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.image
        return kwargs

    def test_func(self):
        if self.request.user.is_authenticated:
            iid = self.kwargs.get('image_id', None)
            logging.warning(iid)
            if iid is not None:
                self.image = get_object_or_404(Images, pk=iid)
                self.gallery = self.image.gallery
                self.success_url = reverse_lazy('photo:image', kwargs={'image_id': iid})
            return self.request.user.is_staff
        else:
            return False
