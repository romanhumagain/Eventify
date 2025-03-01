from django.shortcuts import render
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import Event, EventCategory  
from .serializers import EventSerializer, EventCategorySerializer
from rest_framework import generics
from datetime import datetime, timedelta

# to handle the event category
class EventCategoryViewSet(ModelViewSet):
    queryset = EventCategory.objects.all()
    serializer_class = EventCategorySerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        # check if the user is an admin 
        if not request.user.is_superuser:
            return Response({"error": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)
      
    def update(self, request, *args, **kwargs):
        # check if the user is an admin 
        if not request.user.is_superuser:
            return Response({"error": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
      
    def destroy(self, request, *args, **kwargs):
        # check if the user is an admin 
        if not request.user.is_superuser:
            return Response({"error": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

# to list the available events
class EventListCreateAPIView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = Event.objects.filter(is_approved=True, start_date__gte=datetime.now()).order_by("start_date")
        category = self.request.query_params.get("category")
        date_filter = self.request.query_params.get("date")
        event_type = self.request.query_params.get("type")
        price_filter = self.request.query_params.get("price")
        scope = self.request.query_params.get("scope")

        if category:
            queryset = queryset.filter(category__name=category)
        if date_filter == "today":
            queryset = queryset.filter(start_date__date=datetime.now().date())
        elif date_filter == "tomorrow":
            queryset = queryset.filter(start_date__date=(datetime.now() + timedelta(days=1)).date())
        elif date_filter == "this_week":
            queryset = queryset.filter(start_date__week=datetime.now().isocalendar()[1])
        elif date_filter == "this_month":
            queryset = queryset.filter(start_date__month=datetime.now().month)
        if event_type == "online":
            queryset = queryset.filter(is_online=True)
        elif event_type == "physical":
            queryset = queryset.filter(is_online=False)
        if price_filter == "free":
            queryset = queryset.filter(price=0)
        elif price_filter == "paid":
            queryset = queryset.exclude(price=0)
        if scope == "my_events":
            queryset = queryset.filter(organizer=self.request.user)

        return queryset

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)
      
# to retrieve, update and delete an event
class EventRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"
    
    def get_queryset(self):
        return super().get_queryset().filter(organizer=self.request.user)
     
    def retrieve(self, request, *args, **kwargs):
        event_id = kwargs["id"]
        event = Event.objects.get(id=event_id)
        serializer = self.get_serializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        event_id = kwargs["id"]
        event = Event.objects.get(id=event_id)
        serializer = self.get_serializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
    def destroy(self, request, *args, **kwargs):
        event_id = kwargs["id"]
        event = Event.objects.get(id=event_id)
        event.delete()
        return Response({"detail": "Event deleted successfully."}, status=status.HTTP_200_OK)
      
    
    
