from django.contrib.auth import get_user_model
from rest_framework import serializers
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        # exclude = []
        fields = ['first_name', 'last_name', 'city', 'post_code', 'phone', 'state', 'street', 'dob', 'nickname',
                  'is_model', 'is_photographer']
        extra_kwargs = {}
        for field in fields[:-3]:
            extra_kwargs[field] = {'required': True}
