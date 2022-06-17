# from django.contrib.auth.mixins import LoginRequiredMixin
# from rest_framework.views import APIView
# from rest_framework import permissions, status
# from rest_framework.response import Response
#
# from ..serializers import ImageSerializer
#
# import logging
# logger = logging.getLogger(__name__)
#
#
# class ImageApiView(LoginRequiredMixin, APIView):
#     permission_classes = [permissions.IsAuthenticated]
#
#     def post(self, request, gallery_id):
#         logging.debug(request.data)
#
#         serializer = ImageSerializer(data=request.data)
#         if serializer.is_valid():
#             image_form = serializer.save()
#
#             return Response(serializer.data)
#
#         else:
#             logging.debug(serializer.errors)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
