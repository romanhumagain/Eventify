# payments/urls.py
from django.urls import path
from .views import CreatePaymentIntentView, PaymentVerifyView, PaymentCancelView

urlpatterns = [
    path('create-payment-intent/', CreatePaymentIntentView.as_view(), name='create-payment-intent'),
    path('verify/', PaymentVerifyView.as_view(), name='payment_success'),
    path('cancel/', PaymentCancelView.as_view(), name='payment_cancel'),
]