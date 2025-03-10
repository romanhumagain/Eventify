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
from .serializers import (
    EventSerializer,
    EventCategorySerializer,
    SavedEventSerializer,
    EventDetailsSerializer
)
from rest_framework import generics
from datetime import timedelta
from .permissions import IsOwnerOrReadOnly, IsSuperuserOrReadOnly
from django.utils import timezone
from datetime import timedelta
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Case, When, Value, IntegerField
from django.db.models import Max, F
from django.db import models



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
        now = timezone.now()

        queryset = (
            Event.objects.filter(is_approved=True)
            .annotate(
                event_status=Case(
                    When(
                        start_date__lte=now, end_date__gte=now, then=Value(1)
                    ),  # Active events
                    When(start_date__gt=now, then=Value(2)),  # Upcoming events
                    When(end_date__lt=now, then=Value(3)),  # Expired events
                    default=Value(3),
                    output_field=IntegerField(),
                )
            )
            .order_by("event_status", "start_date", "-end_date")
        )
        
        # Get filters from query params
        search_query = self.request.query_params.get("search")
        category_filter = self.request.query_params.get("category")
        date_filter = self.request.query_params.get("date")
        event_type = self.request.query_params.get("event_type")
        is_free = self.request.query_params.get("is_free")
        location_filter = self.request.query_params.get("venue")
        status_filter = self.request.query_params.get("status")


        # Search filter
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)
            
        # Category filter - case-insensitive matching
        if category_filter:
            queryset = queryset.filter(category__name__icontains=category_filter)

        now = timezone.now()
        if status_filter == "upcoming":
            # Include both upcoming and active events
            queryset = queryset.filter(
                (models.Q(start_date__gt=now) |  # Upcoming events
                 models.Q(start_date__lte=now, end_date__gte=now))  # Active events
            )
        elif status_filter == "active":
            queryset = queryset.filter(
                start_date__lte=now,
                end_date__gte=now
            )
        elif status_filter == "expired":
            queryset = queryset.filter(
                end_date__lt=now
            )
            
        # Date filters
        if date_filter == "today":
            # Get the start and end of today in the current timezone
            today_start = timezone.now().replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            today_end = today_start + timedelta(days=1)
            queryset = queryset.filter(
                start_date__gte=today_start, start_date__lt=today_end
            )

        elif date_filter == "tomorrow":
            # Get the start and end of tomorrow in the current timezone
            tomorrow_start = (timezone.now() + timedelta(days=1)).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            tomorrow_end = tomorrow_start + timedelta(days=1)
            queryset = queryset.filter(
                start_date__gte=tomorrow_start, start_date__lt=tomorrow_end
            )

        elif date_filter == "this_week":
            # Get the start of the current week (Monday)
            now = timezone.now()
            start_of_week = now.replace(
                hour=0, minute=0, second=0, microsecond=0
            ) - timedelta(days=now.weekday())
            end_of_week = start_of_week + timedelta(days=7)
            queryset = queryset.filter(
                start_date__gte=start_of_week, start_date__lt=end_of_week
            )

        elif date_filter == "next_week":
            # For testing - include next week too
            now = timezone.now()
            start_of_week = now.replace(
                hour=0, minute=0, second=0, microsecond=0
            ) - timedelta(days=now.weekday())
            end_of_week = start_of_week + timedelta(days=14)  # Two weeks instead of one
            queryset = queryset.filter(
                start_date__gte=start_of_week, start_date__lt=end_of_week
            )

        elif date_filter == "this_month":
            # Get the start and end of the current month
            now = timezone.now()
            start_of_month = now.replace(
                day=1, hour=0, minute=0, second=0, microsecond=0
            )
            if now.month == 12:
                next_month = now.replace(year=now.year + 1, month=1, day=1)
            else:
                next_month = now.replace(month=now.month + 1, day=1)
            queryset = queryset.filter(
                start_date__gte=start_of_month, start_date__lt=next_month
            )

        # Event type filter
        if event_type == "remote":
            queryset = queryset.filter(event_type__icontains="remote")
        elif event_type == "physical":
            queryset = queryset.filter(event_type__icontains="physical")

        # Price filter
        # Apply filter for 'is_free' if not empty
        if is_free is not None and is_free.lower() in ['true', 'false']:
            queryset = queryset.filter(is_free=is_free.lower() == 'true')

        # location filter
        if location_filter:
            queryset = queryset.filter(venue__icontains=location_filter)

        return queryset

    def perform_create(self, serializer):
        # Save the event with the organizer as the current user and is_approved = False
        try:
            serializer.save(organizer=self.request.user, is_approved=False)
        except IntegrityError:
            raise ValidationError(
                {
                    "detail": "An event with this title, start date and event type already exists."
                }
            )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

# to list all the self posted event (filter option for is_approved or not )
class MyEventListAPIView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
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
            
        queryset = queryset.order_by('-created_at')
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


# to retrieve spicific event, update and delete an event
class EventRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventDetailsSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = "id"

    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context
    
    def delete(self, request, *args, **kwargs):
        event = self.get_object()
        
        if event.tickets.filter(status='paid').exists():
            return Response(
                {"error": "You cannot delete this event because user has already booked it."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().delete(request, *args, **kwargs)


# for saving and unsaving events
class SavedEventToggleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        """Save or Unsave an event."""
        event = get_object_or_404(Event, id=event_id, is_approved=True)
        saved_event, created = SavedEvent.objects.get_or_create(
            user=request.user, event=event
        )

        if created:
            return Response(
                {"detail": "Event saved successfully."}, status=status.HTTP_200_OK
            )
        else:
            saved_event.delete()
            return Response(
                {"detail": "Event unsaved successfully."}, status=status.HTTP_200_OK
            )

# to get list of saved events
class SavedEventListAPIView(generics.ListAPIView):
    serializer_class = SavedEventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = SavedEvent.objects.filter(
            user=self.request.user, event__is_approved=True
        ).order_by("-saved_at")
        
        # Get filters from query params
        search_query = self.request.query_params.get("search")
        category_filter = self.request.query_params.get("category")
        date_filter = self.request.query_params.get("date")
        event_type = self.request.query_params.get("event_type")
        is_free = self.request.query_params.get("is_free")
        location_filter = self.request.query_params.get("venue")
        status_filter = self.request.query_params.get("status")
        

        # Search filter - apply to event title instead of SavedEvent
        if search_query:
            queryset = queryset.filter(event__title__icontains=search_query)
            
        # Category filter - apply to event's category
        if category_filter:
            queryset = queryset.filter(event__category__name__icontains=category_filter)

        # Filter by event status (upcoming, active, expired)
        now = timezone.now()
        if status_filter == "upcoming":
            # Include both upcoming and active events
            queryset = queryset.filter(
                (models.Q(event__start_date__gt=now) |  # Upcoming events
                 models.Q(event__start_date__lte=now, event__end_date__gte=now))  # Active events
            )
        elif status_filter == "active":
            queryset = queryset.filter(
                event__start_date__lte=now,
                event__end_date__gte=now
            )
        elif status_filter == "expired":
            queryset = queryset.filter(
                event__end_date__lt=now
            )
            
        # Date filters - apply to event's start_date
        if date_filter == "today":
            today_start = timezone.now().replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            today_end = today_start + timedelta(days=1)
            queryset = queryset.filter(
                event__start_date__gte=today_start, event__start_date__lt=today_end
            )

        elif date_filter == "tomorrow":
            tomorrow_start = (timezone.now() + timedelta(days=1)).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            tomorrow_end = tomorrow_start + timedelta(days=1)
            queryset = queryset.filter(
                event__start_date__gte=tomorrow_start, event__start_date__lt=tomorrow_end
            )

        elif date_filter == "this_week":
            now = timezone.now()
            start_of_week = now.replace(
                hour=0, minute=0, second=0, microsecond=0
            ) - timedelta(days=now.weekday())
            end_of_week = start_of_week + timedelta(days=7)
            queryset = queryset.filter(
                event__start_date__gte=start_of_week, event__start_date__lt=end_of_week
            )

        elif date_filter == "next_week":
            now = timezone.now()
            start_of_week = now.replace(
                hour=0, minute=0, second=0, microsecond=0
            ) - timedelta(days=now.weekday())
            end_of_week = start_of_week + timedelta(days=14)  # Two weeks instead of one
            queryset = queryset.filter(
                event__start_date__gte=start_of_week, event__start_date__lt=end_of_week
            )

        elif date_filter == "this_month":
            now = timezone.now()
            start_of_month = now.replace(
                day=1, hour=0, minute=0, second=0, microsecond=0
            )
            if now.month == 12:
                next_month = now.replace(year=now.year + 1, month=1, day=1)
            else:
                next_month = now.replace(month=now.month + 1, day=1)
            queryset = queryset.filter(
                event__start_date__gte=start_of_month, event__start_date__lt=next_month
            )

        # Event type filter - apply to event's event_type
        if event_type == "remote":
            queryset = queryset.filter(event__event_type__icontains="remote")
        elif event_type == "physical":
            queryset = queryset.filter(event__event_type__icontains="physical")

        # Price filter - apply to event's is_free
        if is_free is not None and is_free.lower() in ['true', 'false']:
            queryset = queryset.filter(event__is_free=is_free.lower() == 'true')

        # location filter - apply to event's venue
        if location_filter:
            queryset = queryset.filter(event__venue__icontains=location_filter)
    
        return queryset


# to get all my booking 
class MyBookingAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):

        events_with_latest_booking = Event.objects.filter(
            tickets__user=request.user, 
            tickets__status="paid",
            is_approved = True
        ).annotate(
            latest_booking_date=Max('tickets__purchase_date')
        ).order_by('-latest_booking_date').distinct()
        
        # Serialize the events
        serializer = EventSerializer(events_with_latest_booking, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
