from django.contrib import admin
from .models import Notification

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'message_summary', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'event__title', 'message')
    readonly_fields = ('created_at',)

    def message_summary(self, obj):
        """Show a short preview of the message"""
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message
    message_summary.short_description = 'Message'

admin.site.register(Notification, NotificationAdmin)
