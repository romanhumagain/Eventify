from django.contrib import admin
from .models import Ticket, TicketQR
from django.utils.html import format_html

class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_code', 'event', 'user', 'quantity', 'total_price', 'status', 'purchase_date')
    list_filter = ('status', 'event')
    search_fields = ('ticket_code', 'event__title', 'user__first_name', 'user__last_name')
    ordering = ('-purchase_date',)
    readonly_fields = ('ticket_code', 'purchase_date')

# Register the customized admin for Ticket model
admin.site.register(Ticket, TicketAdmin)

@admin.register(TicketQR)
class TicketQRAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'user', 'event', 'is_checked_in', 'checked_in_time', 'qr_code_preview')
    list_filter = ('is_checked_in', 'ticket__event')
    search_fields = ('ticket__ticket_code', 'ticket__user__username', 'ticket__event__title')
    # readonly_fields = ('ticket', 'qr_code_data', 'qr_code_image', 'is_checked_in', 'checked_in_time', 'qr_code_preview')

    def user(self, obj):
        return obj.ticket.user.username

    def event(self, obj):
        return obj.ticket.event.title

    def qr_code_preview(self, obj):
        if obj.qr_code_image:
            return format_html('<img src="{}" width="80" height="80" style="border-radius:10px;"/>', obj.qr_code_image.url)
        return "No QR Code"

    qr_code_preview.short_description = "QR Code Preview"
