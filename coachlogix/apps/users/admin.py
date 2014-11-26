from django.contrib import admin

from . import models


class ProfileAdmin(admin.ModelAdmin):
    fields = ('user', 'nickname',)
    readonly_fields = ('user',)


admin.site.register(models.User)
admin.site.register(models.Profile, ProfileAdmin)
admin.site.register(models.Role)
