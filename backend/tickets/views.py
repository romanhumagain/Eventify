from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from.models import  BookedTicket
from django.utils import timezone

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
            ticket_qr = BookedTicket.objects.select_related('ticket', 'ticket__event').get(qr_code_data=qr_code_data)
        except BookedTicket.DoesNotExist:
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
     
        valid_statuses = ['paid']
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
                'ticket_quantity':ticket_qr.ticket.quantity,
                'ticket_status':ticket_qr.ticket.status,
                'purchase_date':ticket_qr.ticket.purchase_date,
                'attendee_name': ticket_qr.ticket.user.username,
                'check_in_time': ticket_qr.checked_in_time.strftime("%Y-%m-%d %H:%M:%S")
            }
        }, status=status.HTTP_200_OK)
        
        