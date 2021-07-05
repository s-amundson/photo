from django.utils.datetime_safe import datetime
from rest_framework import serializers
from PIL import Image
from ..models import Images
import logging
logger = logging.getLogger(__name__)


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Images
        # exclude = []
        fields = ['image', 'gallery']

    def save(self, *args, **kwargs):
        if self.instance is not None:
            if self.instance.image:
                self.instance.image.delete()
        for k, v in kwargs.items():
            logging.debug(f'k={k}, v={v}')
        # logging.debug(self.image)
        image = self.validated_data.get('image')
        img = Image.open(self.validated_data.get('image'))
        w, h = img.size
        logging.debug(f'width= {w}, height= {h}')
        exif = img.getexif()
        logging.debug(exif)
        taken = datetime.strptime(exif[306], '%Y:%m:%d %H:%M:%S') #“2017:09:29 17:36:00”
        g = self.validated_data.get('gallery')
        logging.debug(g)

        return super().save(image=image, height=h, width=w, thumb_width=100, orientation=exif[274], taken=taken,
                            camera_make=exif[271], camera_model=exif[272], *args, **kwargs)
