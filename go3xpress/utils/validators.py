from __future__ import absolute_import

import os

import magic
from django.core.exceptions import ValidationError


def validate_uploaded_image_extension(value):
    valid_mime_types = ["image/svg+xml", "image/jpeg", "image/png"]
    file_mime_type = magic.from_buffer(value.read(2048), mime=True)
    if file_mime_type not in valid_mime_types:
        raise ValidationError("Unsupported image file type.")
    valid_file_extensions = [".svg", ".jpg", ".png"]
    ext = os.path.splitext(value.name)[1]
    if ext.lower() not in valid_file_extensions:
        raise ValidationError("Unacceptable image file extension.")


def validate_uploaded_pdf_extension(value):
    valid_mime_types = ["image/jpeg", "application/pdf"]
    file_mime_type = magic.from_buffer(value.read(2048), mime=True)
    if file_mime_type not in valid_mime_types:
        raise ValidationError("Unsupported upload file type.")
    valid_file_extensions = [".pdf", ".jpg"]
    ext = os.path.splitext(value.name)[1]
    if ext.lower() not in valid_file_extensions:
        raise ValidationError("Unacceptable pdf/jpg file extension.")


def validate_uploaded_zip_extension(value):
    valid_mime_types = ["application/x-7z-compressed", "application/gzip", "application/zip"]
    file_mime_type = magic.from_buffer(value.read(2048), mime=True)
    if file_mime_type not in valid_mime_types:
        raise ValidationError("Unsupported upload file type.")
    valid_file_extensions = [".zip", ".7z", ".gz"]
    ext = os.path.splitext(value.name)[1]
    if ext.lower() not in valid_file_extensions:
        raise ValidationError("Unacceptable Gzip/zip/7z file extension.")

