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
        fields = ['image', 'gallery', 'height', 'width', 'thumb_width']
        extra_kwargs = {'height': {'required': False}, 'width': {'required': False}, 'thumb_width': {'required': False}}

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
        taken = exif.get(306, None)
        if taken is not None:
            taken = datetime.strptime(taken, '%Y:%m:%d %H:%M:%S') #“2017:09:29 17:36:00”
        g = self.validated_data.get('gallery')
        logging.debug(g)

        return super().save(image=image, height=h, width=w, thumb_width=100, orientation=exif.get(274, 0), taken=taken,
                            camera_make=exif.get(271, 'None'), camera_model=exif.get(272, 'None'), *args, **kwargs)
