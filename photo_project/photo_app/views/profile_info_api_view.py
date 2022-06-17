import logging

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from ..serializers import ProfileSerializer
from ..models import User
logger = logging.getLogger(__name__)


class PhotoModelApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        logging.debug(request.user)
        get_object_or_404(User, pk=request.user.pk)
        serializer = ProfileSerializer(instance=get_object_or_404(User, pk=request.user.pk))
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProfileSerializer(data=request.data, instance=request.user)

        if serializer.is_valid():
            logging.debug(serializer.validated_data)
            serializer.save()

            return Response({'status': 'SUCCESS'})

        else:
            logging.debug(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
