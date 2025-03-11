from django.contrib import admin
from .models import Feedback

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("event_title", "event_organizer", "user_username", "message")

    def event_title(self, obj):
        return obj.event.title
    event_title.admin_order_field = 'event__title'  # Allows sorting by event title
    event_title.short_description = 'Event Title'   # Customize column header in admin

    def event_organizer(self, obj):
        return obj.event.organizer
    event_organizer.admin_order_field = 'event__organizer'
    event_organizer.short_description = 'Organizer'

    def user_username(self, obj):
        return obj.user.username
    user_username.admin_order_field = 'user__username'
    user_username.short_description = 'User'

admin.site.register(Feedback, FeedbackAdmin)
