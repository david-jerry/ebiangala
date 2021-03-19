import os
import magic
from django.core.exceptions import ValidationError

def validate_user_photo_extension(value):
    valid_mime_types = ['image/svg+xml', 'image/jpeg', 'image/png']
    file_mime_type = magic.from_buffer(value.read(1024), mime=True)
    if file_mime_type not in valid_mime_types:
        raise ValidationError('Unsupported file type.')
    valid_file_extensions = ['.svh', '.jpg', '.png']
    ext = os.path.splitext(value.name)[1]
    if ext.lower() not in valid_file_extensions:
        raise ValidationError('Unacceptable file extension.')
