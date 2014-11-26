import re
import base64

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import UploadedFile
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from coachlogix.apps.files.utils import (
    get_b64_extension,
    valid_file_extension,
    valid_file_mimetype
)


class FileField(serializers.FileField):

    def from_native(self, data):
        """
        Checks to see if data is a base64 encoded file, or a subclass of Django's
        ``UploadedFile`` and processes it.

        :data: Either a string or an subclass of ``UploadedFile``
        """
        # Check to see if it's a base64 encoded file and validate/process it here.
        if isinstance(data, basestring):
            # Get the file name and extension.
            file_name = "{}.{}".format("b64", get_b64_extension(data))
           
            # Strip out the data header if it exists.
            data = re.sub(r"^data\:.+base64\,(.+)$", r"\1", data)
 
            # Try to base64 decode the data url.
            try:
                decoded = base64.b64decode(data)
            except TypeError:
                raise serializers.ValidationError(_('Not a valid file'))

            # Update the data dict with new values.
            data = ContentFile(decoded, name=file_name)

            return super(FileField, self).from_native(data)
 
        # The upload must be a subclass of ``UploadedFile``, move along to validation.
        elif isinstance(data, UploadedFile):
            return super(FileField, self).from_native(data)
        else:
            raise serializers.ValidationError(_('Invalid file uploaded.'))
