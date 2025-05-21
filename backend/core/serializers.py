import base64
import uuid
import binascii
import imghdr
from rest_framework import serializers
from django.core.files.base import ContentFile
from django.utils.translation import gettext_lazy as _


class Base64ImageField(serializers.ImageField):
    DEFAULT_MAX_SIZE = 5 * 1024 * 1024
    ALLOWED_IMAGE_TYPES = ['jpeg', 'jpg', 'png', 'gif', 'webp']

    default_error_messages = {
        'required': _('Обязательное поле.'),
        'invalid': _('Недопустимый тип файла. Используйте изображение.'),
        'max_size': _(
            'Максимальный размер файла {max_size_mb} MB.'
            'Ваш файл {file_size_mb} MB.'
        ),
        'invalid_image': _(
            'Недопустимое содержимое файла. Файл не является изображением.'
        ),
        'invalid_type': _(
            'Недопустимый тип изображения. Разрешенные типы: {allowed_types}.'
        ),
    }

    def __init__(self, *args, **kwargs):
        self.max_size = kwargs.pop('max_size', self.DEFAULT_MAX_SIZE)
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        if data is None:
            if self.required:
                self.fail('required')
            return None

        if isinstance(data, str) and data.startswith('data:image'):
            try:
                format, imgstr = data.split(';base64,')
                image_type = format.split('/')[-1].lower()

                if image_type not in self.ALLOWED_IMAGE_TYPES:
                    self.fail(
                        'invalid_type',
                        allowed_types=', '.join(self.ALLOWED_IMAGE_TYPES)
                    )

                decoded_file = base64.b64decode(imgstr)

                image_format = imghdr.what(None, h=decoded_file)
                if not image_format:
                    self.fail('invalid_image')

                file_size = len(decoded_file)
                if file_size > self.max_size:
                    self.fail(
                        'max_size',
                        max_size_mb=self.max_size // (1024 * 1024),
                        file_size_mb=file_size // (1024 * 1024) + 1,
                    )

                file_name = f"{uuid.uuid4()}.{image_type}"
                data = ContentFile(decoded_file, name=file_name)

            except (ValueError, AttributeError, TypeError, binascii.Error):
                self.fail('invalid')

        return super().to_internal_value(data)
