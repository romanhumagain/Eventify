from django.urls import path
from .views import (LoginAPIView, 
                    RegisterAPIView, 
                    UserRetriveUpdateDeleteAPIView
                    )
urlpatterns = [
    path('login/',LoginAPIView.as_view(),name='login'),
    path('register/',RegisterAPIView.as_view(),name='register'),
    path('profile/',UserRetriveUpdateDeleteAPIView.as_view(),name='user-profile'),
]