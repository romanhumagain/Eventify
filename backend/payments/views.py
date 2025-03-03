from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import stripe
from django.conf import settings
from django.db import transaction
from .service import StripeService
from events.models import Event
from tickets.models import Ticket, TicketQR
from .models import Payment
import secrets
import hashlib
from django.utils import timezone

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreatePaymentIntentView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Create a payment intent for ticket purchase
        
        Request data:
        {
            "event_id": 123,
            "quantity": 2
        }
        """
        try:
            event_id = request.data.get('event_id')
            quantity = int(request.data.get('quantity', 1))
            
            # Validate event exists and has available tickets
            try:
                event = Event.objects.get(id=event_id)
                
                if event.is_expired():
                    return Response(
                        {'error': 'This event is no longer accepting bookings.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                if event.tickets_available() < quantity:
                    return Response(
                        {'error': f'Only {event.tickets_available()} tickets available.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except Event.DoesNotExist:
                return Response(
                    {'error': 'Event not found.'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Create ticket reservation
            with transaction.atomic():
                # If it's a free event, create a paid ticket immediately
                if event.is_free:
                    ticket = Ticket.objects.create(
                        event=event,
                        user=request.user,
                        quantity=quantity,
                        unit_price=0,
                        total_price=0,
                        status='PAID'  # Free tickets are marked as paid immediately
                    )
                    
                    # Generate QR codes for free tickets
                    self._generate_qr_codes(ticket)
                    
                    # Update event ticket count
                    event.tickets_sold += quantity
                    event.save()
                    
                    return Response({
                        'success': True,
                        'ticket_id': ticket.id,
                        'free_event': True
                    })
                else:
                    # For paid events, create a reservation first
                    ticket = Ticket.objects.create(
                        event=event,
                        user=request.user,
                        quantity=quantity,
                        unit_price=event.price,
                        total_price=event.price * quantity,
                        status='RESERVED'
                    )
                    
                    # Create Stripe Payment Intent
                    payment_intent = StripeService.create_payment_intent(ticket)
                    
                    if 'error' in payment_intent:
                        # If payment creation fails, delete the ticket reservation
                        ticket.delete()
                        return Response(
                            {'error': payment_intent['error']},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    
                    return Response({
                        'success': True,
                        'ticket_id': ticket.id,
                        'client_secret': payment_intent['client_secret'],
                        'payment_intent_id': payment_intent['payment_intent_id'],
                        'publishable_key': settings.STRIPE_PUBLIC_KEY
                    })
                    
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _generate_qr_codes(self, ticket):
        """Generate QR codes for a ticket"""
        for i in range(ticket.quantity):
            # Create a unique, secure identifier for this specific ticket
            unique_string = f"{ticket.id}:{ticket.event.id}:{ticket.user.id}:{i}:{secrets.token_hex(8)}"
            # Use a secure hash to create the QR code data
            qr_code_data = hashlib.sha256(unique_string.encode()).hexdigest()
            
            # Create the QR code record
            TicketQR.objects.create(
                ticket=ticket,
                qr_code_data=qr_code_data,
                is_checked_in=False
            )


class PaymentConfirmationView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Confirm a payment was successful and generate tickets
        
        Request data:
        {
            "payment_intent_id": "pi_123456789",
            "ticket_id": 42
        }
        """
        try:
            payment_intent_id = request.data.get('payment_intent_id')
            ticket_id = request.data.get('ticket_id')
            
            # Validate the ticket exists and belongs to this user
            try:
                ticket = Ticket.objects.get(id=ticket_id, user=request.user)
            except Ticket.DoesNotExist:
                return Response(
                    {'error': 'Ticket not found or does not belong to this user.'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Check if ticket is already paid
            if ticket.status == 'PAID':
                return Response(
                    {'error': 'This ticket has already been paid for.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Verify payment with Stripe
            payment_status = StripeService.confirm_payment(payment_intent_id)
            
            if not payment_status.get('success'):
                return Response(
                    {'error': 'Payment verification failed.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Update ticket and create payment record
            with transaction.atomic():
                # Update ticket status
                ticket.status = 'PAID'
                ticket.save()
                
                # Create payment record
                Payment.objects.create(
                    ticket=ticket,
                    amount=ticket.total_price,
                    payment_method='Credit Card',
                    transaction_id=payment_intent_id,
                    status='COMPLETED'
                )
                
                # Update event ticket count
                event = ticket.event
                event.tickets_sold += ticket.quantity
                event.save()
                
                # Generate QR codes
                qr_codes = []
                for i in range(ticket.quantity):
                    # Create a unique, secure identifier for this specific ticket
                    unique_string = f"{ticket.id}:{event.id}:{request.user.id}:{i}:{secrets.token_hex(8)}"
                    # Use a secure hash to create the QR code data
                    qr_code_data = hashlib.sha256(unique_string.encode()).hexdigest()
                    
                    # Create the QR code record
                    qr = TicketQR.objects.create(
                        ticket=ticket,
                        qr_code_data=qr_code_data,
                        is_checked_in=False
                    )
                    qr_codes.append(qr_code_data)
                
                return Response({
                    'success': True,
                    'ticket_id': ticket.id,
                    'event_name': event.title,
                    'purchase_date': timezone.now(),
                    'quantity': ticket.quantity,
                    'total_price': float(ticket.total_price),
                    'qr_codes': qr_codes
                })
                
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
