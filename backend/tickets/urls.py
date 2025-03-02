from django.urls import path
from .views import PurchaceTicketAPIView, CancelTicketAPIView

urlpatterns = [
    path('purchase/', PurchaceTicketAPIView.as_view(), name='purchase_ticket'), 
    path('cancel/<int:ticket_id>/', CancelTicketAPIView.as_view(), name='cancel_ticket'), 
]
