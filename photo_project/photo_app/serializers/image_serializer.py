from rest_framework import serializers
from ..models import Images
from ..src.img import Img
import logging
logger = logging.getLogger(__name__)


class ImageSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    filename = serializers.ReadOnlyField()

    class Meta:
        model = Images
        # exclude = []
        fields = ['filename', 'id', 'image', 'gallery', 'height', 'width', 'thumb', 'thumb_width', 'privacy_level']
        extra_kwargs = {'height': {'required': False}, 'width': {'required': False}, 'thumb': {'required': False},
                        'thumb_width': {'required': False}}

    def save(self, *args, **kwargs):
        if self.instance is not None:
            if self.instance.image:  # pragma: no cover
                self.instance.image.delete()

        image = self.validated_data.get('image')

        img = Img(image)
        ir = super().save(image=image,
                          height=img.height,
                          width=img.width,
                          thumb_width=200,
                          orientation=img.exif.get(274, 0),
                          taken=img.taken,
                          camera_make=img.exif.get(271, 'None'),
                          camera_model=img.exif.get(272, 'None'),
                          thumb=img.img_file,
                          filename=image.name, *args, **kwargs)
        ir.save()
        return ir
