from django.contrib import admin
from .models import Feedback

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("event__title","event__organizer", "user__username", "rating")  

admin.site.register(Feedback, FeedbackAdmin)