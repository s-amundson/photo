import logging

from django.core.mail import EmailMessage
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from ..serializers import ProfileSerializer
from ..models import User
logger = logging.getLogger(__name__)


class PhotoModelApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        try:
            pm = User.objects.filter(user=request.user).values()[0]
            pm['first_name'] = request.user.first_name
            pm['last_name'] = request.user.last_name
        except IndexError:
            pm = None
        logging.debug(pm)
        serializer = ProfileSerializer(instance=pm)
        return Response(serializer.data)

    def post(self, request, format=None):
        try:
            pm = User.objects.get(user=request.user)
        except User.DoesNotExist:
            pm = None
        serializer = ProfileSerializer(data=request.data, instance=pm,
                                       initial={'first_name': request.user.first_name,
                                                   'last_name': request.user.last_name})

        if serializer.is_valid():
            logging.debug(serializer.validated_data)
            pm = serializer.save(user=request.user)

            return Response({'status': 'SUCCESS'})

        else:
            logging.debug(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
