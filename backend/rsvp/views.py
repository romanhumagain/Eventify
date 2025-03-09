from rest_framework import viewsets
from .models import RSVP
from .serializers import RSVPSerializer
from rest_framework.permissions import IsAuthenticated
from datetime import timedelta
from django.utils.timezone import now
from tickets.models import Ticket
from django.core.mail import send_mail
from django.conf import settings


class RSVPViewSet(viewsets.ModelViewSet):
    queryset = RSVP.objects.all()
    serializer_class = RSVPSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user) 

    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 
        
# @shared_task
def send_event_reminders():
    today = now().date()
    reminder_date = today + timedelta(days=1)
    
    tickets = Ticket.objects.filter(event__start_date__date = reminder_date)
    
    for ticket in tickets:
        user_email = ticket.user.email
        event = ticket.event
        
        subject = f"Reminder: Your Event '{event.title}' is in 3 Days!"
        message = f"Hello {ticket.user.username},\n\n" \
                  f"This is a reminder that you have registered for '{event.title}' " \
                  f"which is happening on {event.start_date.strftime('%Y-%m-%d %H:%M')}.\n\n" \
                  f"Location: {event.location or 'Online'}\n\n" \
                  f"We look forward to seeing you there!"

        send_mail(subject, message, settings.EMAIL_HOST_USER, [user_email])
        
    return f"Sent {len(tickets)} reminder emails."
        
       
