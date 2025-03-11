from django.contrib import admin
from .models import Payment

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'status', 'transaction_id', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'transaction_id', 'ticket__id')
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Payment, PaymentAdmin)
