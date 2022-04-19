import io

from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.datetime_safe import datetime
from PIL import Image

import logging
logger = logging.getLogger(__name__)


class Img:
    def __init__(self, image):
        self.img = Image.open(image)
        self.width, self.height = self.img.size
        logging.debug(f'width= {self.width}, height= {self.height}')
        self.exif = self.img.getexif()
        logging.debug(self.exif)
        self.taken = self.exif.get(306, None)
        if self.taken is not None:
            self.taken = datetime.strptime(self.taken, '%Y:%m:%d %H:%M:%S') #“2017:09:29 17:36:00”

        self.img.thumbnail((200, 200))
        byte_arr = io.BytesIO()
        self.img.save(byte_arr, format=self.img.format)

        cf = ContentFile(self.image_to_byte_array(self.img))
        self.img_file = InMemoryUploadedFile(
            cf,             # file
            None,           # field_name
            image.name,     # file name
            'image/jpeg',   # content_type
            cf.tell,        # size
            None)           # content_type_extra

    def image_to_byte_array(self, img):
        byte_arr = io.BytesIO()
        img.save(byte_arr, format=img.format)
        byte_arr = byte_arr.getvalue()
        return byte_arr

    def update_record(self, record):
        record.width, record.height = self.img.size
        name = record.image.name.split('/')
        logging.info(name)
        record.filename = name[-1]
        record.thumb_width = 200
        record.orientation = self.exif.get(274, 0)
        record.taken = self.taken
        record.camera_make = self.exif.get(271, 'None')
        record.camera_model = self.exif.get(272, 'None')
        record.thumb = self.img_file
        record.save()
