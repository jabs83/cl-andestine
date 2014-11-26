from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from coachlogix.apps.engagements.models import Engagement

from . import models


class EngagementInline(admin.TabularInline):
    model = Engagement
    fk_name = 'emperor'
    extra = 0


class ProctoredEngagementInline(admin.TabularInline):
    extra = 0
    fk_name = 'proctor'
    fields = ('emperor', 'roadmap', 'start_date', 'end_date', 'status',)
    model = Engagement
    readonly_fields = ('emperor',)
    verbose_name = _('Proctored Engagement')
    verbose_name_plural = _('Proctored Engagements')


class AccountAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'type',
        'plan',
        'created',
    ]
    inlines = (
        EngagementInline,
        ProctoredEngagementInline,
    )
    readonly_fields = ('name', 'type', 'owner',)

    fieldsets = (
        (_('Account Info'), {
            'fields': ('type', 'name', 'owner',)
        }),
    )

    def type(self, obj):
        return obj.type.title()

    def owner(self, obj):
        return obj.owner

    def name(self, obj):
        return obj.name

admin.site.register(models.UserAccount, AccountAdmin)
admin.site.register(models.OrganizationAccount, AccountAdmin)
