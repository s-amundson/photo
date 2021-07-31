import os
from PIL import Image
import PIL.ExifTags
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.forms import model_to_dict

# Create your views here.
from django.views import generic, View
from ..models import Gallery, Images
from ..forms import ImageForm
import logging

# Get an instance of a logger
# logger = logging.getLogger(__name__)


class ImageView(LoginRequiredMixin, View):

    def get(self, request, image_id, *args, **kwargs):
        image = get_object_or_404(Images, pk=image_id)
        # image_data = model_to_dict(image, exclude=['image'])
        i = Image.open(image.image)

        exif = {
            PIL.ExifTags.TAGS[k]: v
            for k, v in i._getexif().items()
            if k in PIL.ExifTags.TAGS
        }
        del exif['MakerNote']
        logging.debug(exif)
        o = exif.get('Orientation', '')
        if o == 1 or o == 3:
            orientation = "Landscape"
        elif o == 8 or o == 6:
            orientation = "Portrait"
        else:
            orientation = o

        image_data = {'Camera': exif.get('Model', ''),
                      'Orientation': orientation,
                      'Taken': exif.get('DateTimeOriginal', ''),
                      'ExposureTime': exif.get('ExposureTime', ''),
                      'F-Stop': exif.get('FNumber', ''),
                      'ISO': exif.get('ISOSpeedRatings', ''),
                      'Focal Length': exif.get('FocalLength', ''),
                      'Film Focal Length': exif.get('FocalLengthIn35mmFilm', ''),
                      'Height': exif.get('ExifImageHeight',''),
                      'Width': exif.get('ExifImageWidth', '')
                      }

        return render(request, 'photo_app/image.html', {'image': image, 'image_data': image_data})


        # {'GPSInfo': {0: b'\x02\x03\x00\x00'}, 'ResolutionUnit': 2, 'ExifOffset': 228, 'Make': 'NIKON CORPORATION',
        # 'Model': 'NIKON D3200', 'Software': 'Ver.1.01 ', 'Orientation': 1, 'DateTime': '2021:07:13 08:52:15',
        # 'YCbCrPositioning': 2, 'XResolution': 300.0, 'YResolution': 300.0, 'ExifVersion': b'0230',
        # 'ComponentsConfiguration': b'\x01\x02\x03\x00', 'CompressedBitsPerPixel': 4.0, 'DateTimeOriginal': '2021:07:13 08:52:15',
        # 'DateTimeDigitized': '2021:07:13 08:52:15', 'ExposureBiasValue': 0.0, 'MaxApertureValue': 5.0, 'MeteringMode': 5,
        # 'LightSource': 0, 'Flash': 0, 'FocalLength': 55.0, 'UserComment': b'ASCII\x00\x00\x00 ', 'ColorSpace': 1,
        # 'ExifImageWidth': 6016, 'ExifInteroperabilityOffset': 37526, 'SceneCaptureType': 0, 'SubsecTime': '90',
        # 'SubsecTimeOriginal': '90', 'SubsecTimeDigitized': '90', 'ExifImageHeight': 4000, 'SubjectDistanceRange': 0,
        # 'SensingMethod': 2, 'FileSource': b'\x03', 'ExposureTime': 0.01, 'FNumber': 5.6, 'SceneType': b'\x01',
        # 'ExposureProgram': 3, 'CFAPattern': b'\x00\x02\x00\x02\x00\x01\x01\x02', 'CustomRendered': 0, 'ISOSpeedRatings': 900,
        # 'ExposureMode': 0, 'FlashPixVersion': b'0100', 'SensitivityType': 2, 'WhiteBalance': 0, 'DigitalZoomRatio': 1.0,
        # 'FocalLengthIn35mmFilm': 82, 'GainControl': 2, 'Contrast': 0, 'Saturation': 0, 'Sharpness': 0}