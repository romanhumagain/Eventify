from django.contrib import admin
from .models import Ticket, TicketQR

class TicketAdmin(admin.ModelAdmin):
    # Define the fields to display in the list view
    list_display = ('ticket_code', 'event', 'user', 'quantity', 'total_price', 'status', 'purchase_date')
    
    # Add filters to the sidebar to filter tickets by status and event
    list_filter = ('status', 'event')
    
    # Add search functionality for ticket code, event, and user
    search_fields = ('ticket_code', 'event__title', 'user__first_name', 'user__last_name')
    
    # Add ordering to sort tickets by purchase date (most recent first)
    ordering = ('-purchase_date',)
    
    # Make some fields read-only (for example, ticket_code and purchase_date)
    readonly_fields = ('ticket_code', 'purchase_date', 'payment_id')

# Register the customized admin for Ticket model
admin.site.register(Ticket, TicketAdmin)

# Register the default admin for TicketQR model
admin.site.register(TicketQR)
