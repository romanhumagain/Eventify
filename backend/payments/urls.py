# payments/urls.py
from django.urls import path
from .views import CreatePaymentIntentView, PaymentConfirmationView

urlpatterns = [
    path('create-payment-intent/', CreatePaymentIntentView.as_view(), name='create-payment-intent'),
    path('confirm-payment/', PaymentConfirmationView.as_view(), name='confirm-payment'),
]