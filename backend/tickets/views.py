from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import TicketSerializer, TicketQRSerializer
from events.models import Event
from rest_framework import status
from rest_framework.views import APIView
from.models import Ticket, TicketQR
from utils.qr_code import _generate_qr_codes, send_qr_code_email
from django.db import transaction
from django.utils import timezone

class PurchaceTicketAPIView(CreateAPIView):
  permission_classes = [IsAuthenticated]
  serializer_class = TicketSerializer
  
  
  def create(self, request, *args, **kwargs):
    data = request.data
    event_id = data.get('event')
    quantity = data.get('quantity', 1)
    
    try:
      event = Event.objects.get(id = event_id)
    except Event.DoesNotExist:
      return Response({'detail':"Event doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)
    
    # check the ticket availability
    available_tickets = event.total_tickets - event.tickets_sold
    if available_tickets < quantity:
       return Response({'detail': f"Only {available_tickets} tickets are available."}, status=status.HTTP_400_BAD_REQUEST)
     
    # Set unit_price and calculate total_price
    data['unit_price'] = event.price
    data['total_price'] = event.price * quantity

    serializer = self.get_serializer(data=data)
    if serializer.is_valid():
      serializer.save(user = request.user)
      
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# API view to handle the free tickets 
class PurchaseFreeTicketAPIView(CreateAPIView):
  permission_classes = [IsAuthenticated]
  serializer_class = TicketSerializer
  
  def create(self, request, *args, **kwargs):
    data = request.data
    event_id = data.get('event')
    quantity = data.get('quantity', 1)
    
    try:
      event = Event.objects.get(id = event_id)
    except Event.DoesNotExist:
      return Response({'detail':"Event doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)
    
    # check the ticket availability
    available_tickets = event.total_tickets - event.tickets_sold
    if available_tickets < quantity:
       return Response({'detail': f"Only {available_tickets} tickets are available."}, status=status.HTTP_400_BAD_REQUEST)
     
    # Set unit_price and calculate total_price
    data['unit_price'] = event.ticket_price
    data['total_price'] = event.ticket_price * quantity
    data['status'] = "Reserved"
    serializer = self.get_serializer(data=data)
    
    if serializer.is_valid():
      with transaction.atomic():
        ticket = serializer.save(user = request.user)
        ticketQR = _generate_qr_codes(ticket=ticket)
        send_qr_code_email(ticket_qr=ticketQR)
        
        return Response({'detail':'Successfully purchased tickets'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CancelTicketAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, ticket_id, *args, **kwargs):
        try:
            ticket = Ticket.objects.get(id=ticket_id, user=request.user)
        except Ticket.DoesNotExist:
            return Response({'detail': "Ticket not found or not owned by this user."}, status=status.HTTP_404_NOT_FOUND)

        if ticket.status == 'Cancelled':
            return Response({'detail': "This ticket is already cancelled."}, status=status.HTTP_400_BAD_REQUEST)

        ticket.status = "Cancelled"
        ticket.save()
        return Response({'detail': 'Ticket successfully cancelled.'}, status=status.HTTP_200_OK)


# to get the ticket history details 
class TicketHistoryAPIView(ListAPIView):
  permission_classes = [IsAuthenticated]
  serializer_class = TicketQRSerializer
  
  def get(self, request, *args, **kwargs):
    ticketQRs = TicketQR.objects.filter(ticket__user = request.user).order_by('is_checked_in')
    serializer = self.get_serializer(ticketQRs, many = True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  
# to validate and checkin QR by the organizer
class ValidateQRAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):

        if not request.user.is_organizer:
          return Response({'detail':'You do not have permission for ticket verification'}, status=status.HTTP_403_FORBIDDEN)

        # Validate input data
        qr_code_data = request.data.get('qr_code_data')
        if not qr_code_data:
            return Response({'detail': "QR code data is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Try to find the QR code in the database
        try:
            ticket_qr = TicketQR.objects.select_related('ticket', 'ticket__event').get(qr_code_data=qr_code_data)
        except TicketQR.DoesNotExist:
            return Response({'detail': "Invalid QR code"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the event date is valid
        event = ticket_qr.ticket.event
        if request.user != event.organizer:
          return Response({'detail':'You do not have permission to verify this ticket.'}, status=status.HTTP_403_FORBIDDEN)
        
        # Check if the ticket is already checked in
        if ticket_qr.is_checked_in:
            return Response({
                'detail': "Ticket already checked in",
                'checked_in_time': ticket_qr.checked_in_time.strftime("%Y-%m-%d %H:%M:%S") if ticket_qr.checked_in_time else None
            }, status=status.HTTP_400_BAD_REQUEST)
        
       
        current_date = timezone.now().date()
        
        if event.end_date.date() < current_date:
            return Response({'detail': "This event has already passed"}, status=status.HTTP_400_BAD_REQUEST)
     
        valid_statuses = ['Reserved', 'Paid']
        if ticket_qr.ticket.status not in valid_statuses:
            return Response({
                'detail': f"Ticket status is {ticket_qr.ticket.status}, which is not valid for check-in",
                'valid_statuses': valid_statuses
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # All validations passed, mark as checked in
        ticket_qr.is_checked_in = True
        ticket_qr.checked_in_time = timezone.now()
        ticket_qr.save()
        
        # Return detailed success response
        return Response({
            'detail': 'Ticket successfully checked in',
            'ticket_info': {
                'event_name': event.title,
                'ticket_code': ticket_qr.ticket.ticket_code,
                'attendee_name': ticket_qr.ticket.user.username,
                'check_in_time': ticket_qr.checked_in_time.strftime("%Y-%m-%d %H:%M:%S")
            }
        }, status=status.HTTP_200_OK)