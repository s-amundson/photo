from rest_framework import serializers
from ..models import Links
import logging
logger = logging.getLogger(__name__)


class LinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Links
        fields = ['category', 'url']
