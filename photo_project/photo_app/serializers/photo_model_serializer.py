from rest_framework import serializers
from ..models import PhotoModel
import logging
logger = logging.getLogger(__name__)


class PhotoModelSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = PhotoModel
        # exclude = []
        fields = ['first_name', 'last_name', 'dob', 'city', 'post_code', 'phone', 'state', 'street']

