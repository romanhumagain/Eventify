from django.contrib import admin
from .models import Event, EventCategory, SavedEvent

admin.site.register(Event) 
admin.site.register(EventCategory)
admin.site.register(SavedEvent)
