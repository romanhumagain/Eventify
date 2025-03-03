from django.shortcuts import render
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from .models import Event, EventCategory, SavedEvent
from .serializers import EventSerializer, EventCategorySerializer, SavedEventSerializer, OwnEventSerializer
from rest_framework import generics
from datetime import timedelta
from .permissions import IsOwnerOrReadOnly, IsSuperuserOrReadOnly
from django.utils import timezone
from datetime import timedelta
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404


# to handle the event category
class EventCategoryViewSet(ModelViewSet):
    queryset = EventCategory.objects.all()
    serializer_class = EventCategorySerializer
    permission_classes = [IsSuperuserOrReadOnly]
    
    
# to list the available events
class EventListCreateAPIView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    # For handling profile picture upload
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        queryset = Event.objects.filter(
            is_approved=True,
            end_date__gt=timezone.now(),
        ).order_by("start_date")

        # Get filters from query params
        category = self.request.query_params.get("category")
        date_filter = self.request.query_params.get("date")
        event_type = self.request.query_params.get("type")
        price_filter = self.request.query_params.get("price")
        location_filter = self.request.query_params.get('location')

        # Category filter - case-insensitive matching
        if category:
            queryset = queryset.filter(category__name__icontains=category)

        # Date filters
        if date_filter == "today":
            # Get the start and end of today in the current timezone
            today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
            today_end = today_start + timedelta(days=1)
            queryset = queryset.filter(start_date__gte=today_start, start_date__lt=today_end)
            
        elif date_filter == "tomorrow":
            # Get the start and end of tomorrow in the current timezone
            tomorrow_start = (timezone.now() + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            tomorrow_end = tomorrow_start + timedelta(days=1)
            queryset = queryset.filter(start_date__gte=tomorrow_start, start_date__lt=tomorrow_end)
            
        elif date_filter == "this_week":
            # Get the start of the current week (Monday)
            now = timezone.now()
            start_of_week = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=now.weekday())
            end_of_week = start_of_week + timedelta(days=7)
            queryset = queryset.filter(start_date__gte=start_of_week, start_date__lt=end_of_week)

        elif date_filter == "next_week":
            # For testing - include next week too
            now = timezone.now()
            start_of_week = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=now.weekday())
            end_of_week = start_of_week + timedelta(days=14)  # Two weeks instead of one
            queryset = queryset.filter(start_date__gte=start_of_week, start_date__lt=end_of_week)
            
        elif date_filter == "this_month":
            # Get the start and end of the current month
            now = timezone.now()
            start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            if now.month == 12:
                next_month = now.replace(year=now.year+1, month=1, day=1)
            else:
                next_month = now.replace(month=now.month+1, day=1)
            queryset = queryset.filter(start_date__gte=start_of_month, start_date__lt=next_month)
        
        # Event type filter
        if event_type == "online":
            queryset = queryset.filter(event_type__icontains = "online")
        elif event_type == "physical":
            queryset = queryset.filter(event_type__icontains = "physical")

        # Price filter
        if price_filter == "free":
            queryset = queryset.filter(price=0)
        elif price_filter == "paid":
            queryset = queryset.exclude(price=0)
            
        # location filter
        if location_filter:
            queryset = queryset.filter(location__contains = location_filter)

        return queryset

    def perform_create(self, serializer):
        # Save the event with the organizer as the current user and is_approved = False
        serializer.save(organizer=self.request.user, is_approved=False)


# to list all the self posted event (filter option for is_approved or not )
class MyEventListAPIView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = OwnEventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset().filter(organizer=self.request.user)

        is_approved_filter = self.request.query_params.get("is_approved")

        # Apply filter if 'is_approved' is provided and valid
        if is_approved_filter is not None:
            if is_approved_filter.lower() == "true":
                queryset = queryset.filter(is_approved=True)
            elif is_approved_filter.lower() == "false":
                queryset = queryset.filter(is_approved=False)
            else:
                pass

        return queryset
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request 
        return context
    
    


# to retrieve spicific event, update and delete an event
class EventRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = OwnEventSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = "id"

    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request 
        return context
    
    
  
    
# for saving and unsaving events
class SavedEventToggleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        """Save or Unsave an event."""
        event = get_object_or_404(Event, id=event_id)
        saved_event, created = SavedEvent.objects.get_or_create(user=request.user, event=event)

        if created:
            return Response(
                {"detail": "Event saved successfully."},
                status=status.HTTP_201_CREATED
            )
        else:
            saved_event.delete()
            return Response(
                {"detail": "Event unsaved successfully."},
                status=status.HTTP_200_OK
            )


class SavedEventListAPIView(generics.ListAPIView):
    serializer_class = SavedEventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SavedEvent.objects.filter(user=self.request.user).order_by('saved_at')
