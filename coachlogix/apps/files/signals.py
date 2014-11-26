from django.db.models import signals

from . import models


def process_file_upload(sender, instance, **kwargs):
    """
    Initiate pre-save processing for a newly uploaded file including
    setting a UUID and saving the original file upload name.
    """
    if isinstance(instance, models.File):
        instance._process_new_upload()
