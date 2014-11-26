from django.utils.translation import ugettext_lazy as _

from rest_framework import exceptions
from rest_framework import status


class BaseException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Unexpected error")

    def __init__(self, detail=None):
        self.detail = detail or self.default_detail


class FileUploadError(BaseException):
    """
    An error that is thrown when something goes wrong with the 
    file upload process.
    """
    pass
