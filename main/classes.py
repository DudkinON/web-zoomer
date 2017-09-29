import os
from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile, UploadedFile
from django.db import models
from w.settings import MEDIA_ROOT

from main.functions import image_resize
from .config import IMAGE_UPLOAD_SIZE, IMAGE_QUALITY


class MyImageField(models.ImageField):
    def save_form_data(self, instance, data):
        """Saving the image

        :param instance:
        :param data:
        :return void:
        """
        if data and isinstance(data, UploadedFile):
            image = image_resize(data, IMAGE_UPLOAD_SIZE)
            new_image = BytesIO()
            image.save(new_image, 'JPEG', quality=IMAGE_QUALITY)
            data = SimpleUploadedFile(data.name, new_image.getvalue(),
                                      data.content_type)
            # remove old file
            previous = u'{}{}'.format(MEDIA_ROOT, instance)
            if os.path.isfile(previous):
                os.remove(previous)
        super(MyImageField, self).save_form_data(instance, data)
