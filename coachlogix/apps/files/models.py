import os
import pytz
import datetime
import hashlib

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from easy_thumbnails.templatetags.thumbnail import thumbnail_url
from easy_thumbnails.fields import ThumbnailerField

from coachlogix.base.api.models import ContentBase, ModelBase, TimeStamped

from . import utils


class ProviderRecord(TimeStamped, ModelBase):
    BOX = 0
    PROVIDER_NAMES = (
        (BOX, _('Box')),
    )
    name = models.IntegerField(_('name'), choices=PROVIDER_NAMES)
    status = models.CharField(_('status'), max_length=50, blank=True)
    doc_id = models.CharField(_('ID'), max_length=300, blank=True)
    doc_type = models.CharField(_('type'), max_length=50, blank=True)
    view_url = models.CharField(_('url'), max_length=500, blank=True)
    view_expiration = models.DateTimeField(_('expiration'), null=True, editable=False)

    class Meta:
        verbose_name = _('Provider Record')
        verbose_name_plural = _('Provider Records')

    def __str__(self):
        return self.get_display_name()

    @property
    def is_view_expired(self):
        """Boolean check for view status."""
        now = datetime.datetime.now(pytz.utc)
        return self.view_expiration < now if self.view_expiration else None


class File(TimeStamped, ContentBase):
    file = ThumbnailerField(_('file'), upload_to=settings.GET_UPLOAD_PATH)
    file_name = models.CharField(_('file name'), max_length=100, default='', blank=True)
    file_name_original = models.CharField(_('original file name'), max_length=500, blank=True)
    sha1 = models.CharField(_('sha1'), max_length=40, default='', blank=True)
    description = models.TextField(_('description'), blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='files',
                              verbose_name=_('owner'),
                              on_delete=models.SET_NULL,
                              null=True, blank=True)

    is_public = models.BooleanField(_('Is Public?'), default=True)
    provider = models.OneToOneField(ProviderRecord,
                                    related_name='file',
                                    verbose_name=_('provider'),
                                    on_delete=models.SET_NULL,
                                    null=True, blank=True)

    class Meta:
        verbose_name = _('file')
        verbose_name_plural = _('files')
    
    def __str__(self):
        return self.file_name

    def _process_new_upload(self):
        """
        This method is called in the pre_save signal for the ``File`` object.
        What it does:
        
        1) Generate a SHA1 for the File.
        2) Set the original file name.
        3) Create a UUID file name and save the file.name and file_name.
        """
        if not self.pk:
            self.sha1 = self.generate_sha1()
        self.file_name_original = self.name
        self.file_name = self.file.name = utils.get_file_name(self)

    def generate_sha1(self):
        """Returns a sha1 hash of the file."""
        hasher = hashlib.sha1()
        file_pos = self.file.tell()
        self.file.seek(0)
        while True:
            buf = self.file.read(104857600)
            if not buf:
                break
            hasher.update(buf)
        self.file.seek(file_pos) # reset file position
        return hasher.hexdigest()

    def get_thumbnail_url(self, alias='default'):
        """Returns the url for a given thumbnail."""
        return thumbnail_url(self.file, alias)

    @property
    def is_image(self):
        """Boolean check for image file."""
        return self.extension in settings.VALID_IMAGE_EXTENSIONS

    @property
    def url(self):
        """Return the url of the ``File.file``"""
        return self.file.url

    @property
    def path(self):
        """Return the path of the ``File.file``"""
        return self.file.path

    @property
    def name(self):
        """Return the name of the ``File.file``"""
        return self.file.name

    @property
    def size(self):
        """Return the size of the ``File.file``"""
        return self.file.size

    @property
    def extension(self):
        """Return the extension of the ``File.file``"""
        return (os.path.splitext(self.file.name)[1]).strip('.')
