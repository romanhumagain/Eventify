from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
  list_display = ("email",'first_name', 'last_name', 'username', 'is_active','is_organizer')
  list_filter = ("is_superuser", "is_active","is_organizer")
  search_fields = ("first_name","last_name", "username", "email")
  readonly_fields = ("password",)
admin.site.register(User, UserAdmin)
