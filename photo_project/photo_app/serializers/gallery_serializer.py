from rest_framework import serializers
from ..models import Gallery
import logging
logger = logging.getLogger(__name__)


class GallerySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Gallery
        # exclude = []
        fields = ['id', 'is_public', 'name', 'owner', 'photographer', 'photo_model', 'public_date', 'shoot_date']
