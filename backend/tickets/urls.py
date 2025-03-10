from django.urls import path
from .views import ValidateQRAPIView

urlpatterns = [ 
    path('booking/check-in/', ValidateQRAPIView.as_view(), name="validate_ticket" ),
]

