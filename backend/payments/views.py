from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from tickets.models import Ticket
from events.models import Event
from payments.models import Payment
import stripe
from utils.qr_code import _generate_qr_codes, send_qr_code_email


class CreatePaymentIntentView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            event_id = request.data.get('event_id')
            quantity = int(request.data.get('quantity', 1))
            
            try:
                event = Event.objects.get(id=event_id)
            
                if event.tickets_available < quantity:
                    return Response(
                        {'error': f'Only {event.tickets_available} tickets available.'},
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
                        status='paid'  
                    )
                    
                    # Generate QR codes for free tickets
                    booked_ticket_qr = _generate_qr_codes(ticket)
                    send_qr_code_email(booked_ticket_qr)
                    context = {
                        'detail': 'Successfully purchased tickets', 
                        'qr_code_data': booked_ticket_qr.qr_code_data, 
                        'ticket_id': ticket.id,
                        'ticket_code': ticket.ticket_code, 
                    }
                    return Response(context, status=status.HTTP_200_OK)
                
                else:
                    # For paid events, create a reservation first
                    ticket = Ticket.objects.create(
                        event=event,
                        user=request.user,
                        quantity=quantity,
                        unit_price=event.ticket_price,
                        total_price=event.ticket_price * quantity,
                        status='reserved' 
                    )
                    
                    # Create a Stripe Checkout Session
                    try:
                        # Convert ticket price to cents for Stripe
                        stripe_amount = int(float(event.ticket_price) * 100)
                        
                        checkout_session = stripe.checkout.Session.create(
                            payment_method_types=['card'],
                            line_items=[{
                                'price_data': {
                                    'currency': 'inr',
                                    'product_data': {
                                        'name': f"Ticket(s) for {event.title}",
                                        'description': f"{quantity} ticket(s) for {event.title}",
                                    },
                                    'unit_amount': stripe_amount,
                                },
                                'quantity': quantity,
                            }],
                            mode='payment',
                            success_url=f"{settings.VITE_BASE_URL}/payment/success?session_id={{CHECKOUT_SESSION_ID}}&ticket_id={ticket.id}",
                            cancel_url=f"{settings.VITE_BASE_URL}/payment/cancel?ticket_id={ticket.id}",
                            metadata={
                                'ticket_id': str(ticket.id),
                                'ticket_code': str(ticket.ticket_code),
                                'user_id': str(request.user.id),
                                'event_id': str(event.id)
                            }
                        )
                        
                        payment = Payment.objects.create(
                            user=request.user, 
                            ticket=ticket, 
                            amount=ticket.total_price, 
                            transaction_id=checkout_session.id
                        )
                        
                        return Response({
                            'checkout_url': checkout_session.url,
                            'session_id': checkout_session.id,
                            'ticket_id': ticket.id,
                            'ticket_code': ticket.ticket_code,
                        }, status=status.HTTP_200_OK)
                        
                    except stripe.error.StripeError as e:
                        # If Stripe payment fails, cancel the ticket reservation
                        ticket.status = 'cancelled'
                        ticket.save()
                        return Response({
                            'error': f'Stripe error: {str(e)}'
                        }, status=status.HTTP_400_BAD_REQUEST)
                    
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
class PaymentVerifyView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            session_id = request.data.get('session_id')
            ticket_id = request.data.get('ticket_id')
            
            if not session_id or not ticket_id:
                return Response(
                    {'error': 'Missing session_id or ticket_id'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Verify the payment with Stripe
            try:
                session = stripe.checkout.Session.retrieve(session_id)
                
                # Check if payment was successful
                if session.payment_status == 'paid':
                    # Update ticket status
                    ticket = Ticket.objects.get(id=ticket_id)
            
                    # Verify ticket belongs to the current user for security
                    if ticket.user != request.user:
                        return Response(
                            {'error': 'Unauthorized access to ticket'},
                            status=status.HTTP_403_FORBIDDEN
                        )
                    
                    ticket.status = 'paid'
                    ticket.save()
                    
                    # Update payment status
                    payment = Payment.objects.get(transaction_id=session_id)
                    payment.status = 'completed'
                    payment.save()
                    
                    # Generate QR codes and send emai
                    booked_ticket_qr = _generate_qr_codes(ticket)
                    send_qr_code_email(booked_ticket_qr)
                    
                    return Response({
                        'detail': 'Payment successful',
                        'qr_code_data': booked_ticket_qr.qr_code_data,
                        'ticket_id': ticket.id,
                        'ticket_code': ticket.ticket_code,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'error': 'Payment not completed',
                        'payment_status': session.payment_status
                    }, status=status.HTTP_400_BAD_REQUEST)
                
            except stripe.error.StripeError as e:
                return Response({
                    'error': f'Stripe error: {str(e)}'
                }, status=status.HTTP_400_BAD_REQUEST)
            except Ticket.DoesNotExist:
                return Response({
                    'error': 'Ticket not found'
                }, status=status.HTTP_404_NOT_FOUND)
            except Payment.DoesNotExist:
                return Response({
                    'error': 'Payment record not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentCancelView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            ticket_id = request.data.get('ticket_id')
            
            if not ticket_id:
                return Response(
                    {'error': 'Missing ticket_id'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                # Cancel the ticket
                ticket = Ticket.objects.get(id=ticket_id)
                
                # Verify ticket belongs to the current user for security
                if ticket.user != request.user:
                    return Response(
                        {'error': 'Unauthorized access to ticket'},
                        status=status.HTTP_403_FORBIDDEN
                    )
                
                # Only cancel if it's in Reserved status
                if ticket.status == 'reserved':
                    ticket.status = 'cancelled'
                    ticket.save()
                    
                    # Also update any associated payment record
                    Payment.objects.filter(ticket=ticket).update(status='cancelled')
                    
                    return Response({
                        'detail': 'Payment cancelled'
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'detail': 'Ticket already processed and cannot be cancelled',
                        'status': ticket.status
                    }, status=status.HTTP_400_BAD_REQUEST)
                
            except Ticket.DoesNotExist:
                return Response({
                    'error': 'Ticket not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)