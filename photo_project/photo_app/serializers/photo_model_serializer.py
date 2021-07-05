from django.contrib.auth import get_user_model
from rest_framework import serializers
from ..models import PhotoModel
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


class PhotoModelSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    dob = serializers.DateField(required=True)
    city = serializers.CharField(required=True)
    post_code = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    state = serializers.CharField(required=True)
    street = serializers.CharField(required=True)

    # def __init__(self, request, *args, **kwargs):
    #     self.fields['first_name'].initial = request.user.first_name
    #     self.fields['last_name'].initial = request.user.last_name
    #     super().__init__(*args, **kwargs)

    def create(self, validated_data):
        logging.debug(validated_data)
        user = validated_data['user']
        # user = User.objects.get(pk=user.id)
        user.first_name = validated_data.pop('first_name')
        user.last_name = validated_data.pop('last_name')
        user.save()
        validated_data['user'] = user

        pm = PhotoModel.objects.create(**validated_data)
        return pm

    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.user.first_name = validated_data.get('first_name', instance.user.first_name)
        instance.user.last_name = validated_data.get('last_name', instance.user.last_name)
        instance.dob = validated_data.get('dob', instance.dob)
        instance.city = validated_data.get('city', instance.city)
        instance.post_code = validated_data.get('post_code', instance.post_code)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.state = validated_data.get('state', instance.state)
        instance.street = validated_data.get('street', instance.street)
        instance.save()

        return instance
