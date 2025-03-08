from django.urls import path
from .views import PurchaceTicketAPIView, PurchaseFreeTicketAPIView, CancelTicketAPIView, TicketHistoryAPIView, ValidateQRAPIView

urlpatterns = [
    path('purchase/', PurchaceTicketAPIView.as_view(), name='purchase_ticket'), 
    path('free-purchase/', PurchaseFreeTicketAPIView.as_view(), name='purchase_free_ticket'), 
    path('cancel/<int:ticket_id>/', CancelTicketAPIView.as_view(), name='cancel_ticket'), 
    path('history/', TicketHistoryAPIView.as_view(), name="ticket_history"),
    path('validate/', ValidateQRAPIView.as_view(), name="validate_ticket" )
]

