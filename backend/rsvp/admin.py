from django.contrib import admin
from .models import RSVP
from django.contrib import admin
from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule


class RSVPAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'status', 'created_at')
    list_filter = ('status', 'event')  
    search_fields = ('user__first_name', 'user__last_name', 'event__title')  
    ordering = ('-created_at',) 
    # readonly_fields = ('user', 'event', 'created_at') 
   

# Register the customized admin
admin.site.register(RSVP, RSVPAdmin)

# admin.site.register(PeriodicTask)
# admin.site.register(IntervalSchedule)
# admin.site.register(CrontabSchedule)
