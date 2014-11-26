from django.core.urlresolvers import reverse


class AdminContentMixin(object):
    """Provides properties and methods related to the admin site."""

    @property
    def admin_url(self):
        return reverse('admin:{}_{}_change'.format(
            self._meta.app_label, self._meta.model_name), args=(self.pk,))

    def admin_photo(self, obj=None, size='default'):
        """Returns a photo thumbnail for the admin."""
        self = obj if obj else self
        if hasattr(self, 'get_thumbnail_url'):
            return '<a class="thumb-'+size+'" href="{}"><img src="{}"></a>'.format(
                self.admin_url, self.get_thumbnail_url(size))
    admin_photo.allow_tags = True
    admin_photo.short_description = 'Photo'
