from django.contrib import admin
from .models import Event, EventCategory, SavedEvent
from django.utils.html import format_html

class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "organizer", "start_date", "is_approved", "banner_preview")
    list_filter = ("is_approved", "start_date", "category")
    search_fields = ("title", "organizer__username")
    ordering = ("start_date",)
    date_hierarchy = "start_date"
    list_editable = ("is_approved",)

    def banner_preview(self, obj):
        if obj.banner:
            return format_html('<img src="{}" width="80" height="50" style="border-radius:10px;"/>', obj.banner.url)
        return "No Image Banner"

admin.site.register(Event, EventAdmin)


class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class SavedEventAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'saved_at')
    list_filter = ('saved_at',)
    search_fields = ('user__username', 'event__title')
    readonly_fields = ('saved_at',)
    

admin.site.register(EventCategory, EventCategoryAdmin)
admin.site.register(SavedEvent, SavedEventAdmin)

