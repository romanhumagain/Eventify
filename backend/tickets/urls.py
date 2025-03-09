from django.urls import path
from .views import PurchaseFreeTicketAPIView, TicketHistoryAPIView, ValidateQRAPIView

urlpatterns = [ 
    path('free-purchase/', PurchaseFreeTicketAPIView.as_view(), name='purchase_free_ticket'),
    path('history/', TicketHistoryAPIView.as_view(), name="ticket_history"),
    path('validate/', ValidateQRAPIView.as_view(), name="validate_ticket" ),
   
]

