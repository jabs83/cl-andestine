from django.contrib import admin

from . import models


class EngagementInline(admin.TabularInline):
    model = models.Membership


class EngagementAdmin(admin.ModelAdmin):
    inlines = (EngagementInline,)


admin.site.register(models.Roadmap)
admin.site.register(models.RoadmapItem)
admin.site.register(models.Engagement, EngagementAdmin)
admin.site.register(models.Membership)
