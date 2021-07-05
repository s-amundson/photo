from rest_framework import serializers
from django.template.loader import get_template
from ..forms import GalleryForm
from ..models import Gallery
import logging
logger = logging.getLogger(__name__)


class GallerySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Gallery
        # exclude = []
        fields = ['id', 'can_public', 'name', 'owner', 'photo_model', 'public_date', 'shoot_date']
