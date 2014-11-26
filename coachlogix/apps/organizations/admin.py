from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from coachlogix.apps.users.models import Role

from . import models


class MembershipInline(admin.TabularInline):
    model = models.Membership
    fk_name = 'organization'
    readonly_fields = ('connected_by', 'is_employee',)
    extra = 0
    fields = ('user', 'role', 'title', 'groups', 'connected_by', 'status', 'is_employee',)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """
        Filter out all non-related groups.
        """
        parent_id = request.META['PATH_INFO'].rstrip('/').split('/')[-1]
        if db_field.name == 'groups' and parent_id.isdigit():
            kwargs['queryset'] = models.Group.objects.filter(organization__pk=int(parent_id))
        return super().formfield_for_manytomany(db_field, request, **kwargs)


class GroupInline(admin.TabularInline):
    model = models.Group
    extra = 0


class RoleInline(admin.TabularInline):
    model = Role
    extra = 0


class OrganizationAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'list_admin_photo',
    ]
    fields = (
        'admin_photo',
        'name',
        'description',
        'avatar',
        'website',
        'location',
        'phone',
        'currency',
        'connected_organizations',
    )
    inlines = (
        RoleInline,
        GroupInline,
        MembershipInline,
    )
    filter_horizontal = ('connected_organizations',)
    readonly_fields = ('admin_photo',)

    def admin_photo(self, obj):
        return obj.avatar.admin_photo()
    admin_photo.allow_tags = True
    admin_photo.short_description = ''

    def list_admin_photo(self, obj):
        if hasattr(obj.avatar, 'admin_photo'):
            return obj.avatar.admin_photo()
    list_admin_photo.allow_tags = True
    list_admin_photo.short_description = 'Avatar'

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """
        Filter out the current parent ``Organization``. Right now we use
        sort of hackish way to get the parent id since there exists
        no other clean way so far.
        """
        parent_id = request.META['PATH_INFO'].rstrip('/').split('/')[-1]
        if db_field.name == 'connected_organizations' and parent_id.isdigit():
            kwargs['queryset'] = models.Organization.objects.exclude(pk=int(parent_id))
        return super().formfield_for_manytomany(db_field, request, **kwargs)


admin.site.register(models.OrganizationDigest)
admin.site.register(models.Organization, OrganizationAdmin)
admin.site.register(models.Group)
admin.site.register(models.Membership)
admin.site.register(models.ProfessionalTitle)
admin.site.register(models.Contact)
