from django.contrib import admin
from .models import Event, EventCategory, SavedEvent
from django.contrib import messages
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "organizer", "start_date", "is_approved")
    list_filter = ("is_approved", "start_date", "category")
    search_fields = ("title", "organizer__username")
    ordering = ("start_date",)
    date_hierarchy = "start_date"
    list_editable = ("is_approved",)

    # def save_model(self, request, obj, form, change):
    #     """Show a message when an event is approved."""
    #     if change:  # Only trigger when updating an event
    #         old_obj = Event.objects.get(pk=obj.pk)
    #         if not old_obj.is_approved and obj.is_approved:
    #             messages.info(request, "Approval process may take a while. Please wait...")
        
    #     super().save_model(request, obj, form, change)

admin.site.register(Event, EventAdmin)

admin.site.register(EventCategory)
admin.site.register(SavedEvent)
