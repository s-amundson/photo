import logging

from django.core.mail import EmailMessage
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from ..serializers import PhotoModelSerializer

logger = logging.getLogger(__name__)


class PhotoModelApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        # response_dict = {'status': 'ERROR', 'receipt_url': '', 'error': '', 'continue': False}
        serializer = PhotoModelSerializer(data=request.data)
        if serializer.is_valid():
            pm = serializer.save(user=request.user)
            pm.user.first_name = serializer.validated_data['first_name']
            pm.user.last_name = serializer.validated_data['last_name']
            return Response(serializer.data)

        else:
            logging.debug(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
