from django.contrib import admin

from . import models


class ProviderRecordAdmin(admin.ModelAdmin):
    fields = (
        'get_name',
        'list_file_name',
        'status',
        'doc_id',
        'doc_type',
        'created',
        'view_url',
        'view_expiration',
    )
    list_display = fields
    readonly_fields = fields

    def get_name(self, obj):
        return obj.get_name_display()
    get_name.short_description = 'Name'

    def file(self, obj):
        return obj.file

    def list_file_name(self, obj):
        return '<a href="{}">{}</a>'.format(obj.file.admin_url, obj.file)
    list_file_name.allow_tags = True
    list_file_name.short_description = 'File'


class FileAdmin(admin.ModelAdmin):
    list_display = (
        'list_admin_photo',
        'list_file_name',
        'provider',
        'owner',
        'created',
        'is_public',
    )
    fields = (
        'admin_photo',
        'file',
        'file_name',
        'file_name_original',
        'path',
        'url',
        'sha1',
        'owner',
        'description',
        'is_public',
        'provider_name',
        'provider_doc_id',
        'provider_status',
    )
    readonly_fields = (
        'admin_photo',
        'file_name',
        'path',
        'url',
        'sha1',
        'provider_name',
        'provider_doc_id',
        'provider_status',
    )
  
    def path(self, obj):
        return obj.path
    path.short_description = 'File path'

    def admin_photo(self, obj):
        return obj.admin_photo()
    admin_photo.allow_tags = True
    admin_photo.short_description = 'Thumbnail'

    def list_admin_photo(self, obj):
        return obj.admin_photo(obj, 'x-small')
    list_admin_photo.allow_tags = True
    list_admin_photo.short_description = 'Photo'

    def list_file_name(self, obj):
        return '<a href="{}">{}</a>'.format(obj.admin_url, obj.file_name)
    list_file_name.allow_tags = True
    list_file_name.short_description = 'File'

    def url(self, obj):
        return obj.url
    url.short_description = 'URL'

    def provider_name(self, obj):
        return obj.provider.get_name_display()
    provider_name.short_description = 'Provider'

    def provider_doc_id(self, obj):
        return obj.provider.doc_id
    provider_doc_id.short_description = 'Provider ID'

    def provider_status(self, obj):
        return obj.provider.status
    provider_status.short_description = 'Provider Status'


admin.site.register(models.File, FileAdmin)
admin.site.register(models.ProviderRecord, ProviderRecordAdmin)
