from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from coachlogix.base.api.serializers import ModelSerializer
from coachlogix.base.api.fields import FileField

from .models import File
from .utils import valid_file_extension, valid_file_mimetype


class FileSerializer(ModelSerializer):
    """File serializer for handling files and images."""
    file = FileField()
    url = serializers.SerializerMethodField('get_url')
    file_size = serializers.SerializerMethodField('get_file_size')
    file_type = serializers.SerializerMethodField('get_file_type')
    thumbnail = serializers.SerializerMethodField('get_thumbnail')
    permissions = serializers.SerializerMethodField('get_permissions')

    class Meta:
        model = File
        owner = serializers.Field(source='owner.pk')
        fields = ('id', 'owner', 'file', 'file_name', 'file_name_original', 'file_size',
                  'file_type', 'url', 'thumbnail', 'description', 'created', 'updated',
                  'permissions',)

    def get_file_size(self, fobj):
        """Return the file size."""
        return fobj.size

    def get_file_type(self, fobj):
        """Return the file type."""
        return fobj.extension

    def get_url(self, fobj):
        """Return the ``File`` url method."""
        return fobj.url

    def get_thumbnail(self, fobj):
        """Return a thumbnail url."""
        return fobj.get_thumbnail_url(settings.THUMBNAIL_DEFAULT_ALIAS)

    def validate(self, data):
        """Verify that it's a proper file and add the name fields to data dict."""
        fobj = data.get('file', None)
        if fobj:
            # Check if it's a valid file type.
            if not valid_file_extension(fobj.name, settings.VALID_FILE_EXTENSIONS)\
                or not valid_file_mimetype(fobj, settings.VALID_FILE_MIMETYPES): 

                # Raise validation error.
                raise serializers.ValidationError(_('Invalid file type.')) 
            return super(FileSerializer, self).validate(data)
        raise serializers.ValidationError(_('No file was found.'))
