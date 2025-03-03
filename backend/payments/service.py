import stripe
from django.conf import settings
from decimal import Decimal

stripe.api_key = settings.STRIPE_SECRET_KEY

class StripeService:
    @staticmethod
    def create_payment_intent(ticket):
        """Create a payment intent for a ticket purchase"""
        try:
            # Convert to cents for Stripe
            amount_cents = int(ticket.total_price * Decimal('100'))
            
            # Create a Payment Intent
            intent = stripe.PaymentIntent.create(
                amount=amount_cents,
                currency='usd',  # Change according to your currency
                metadata={
                    'ticket_id': str(ticket.id),
                    'event_id': str(ticket.event.id),
                    'user_id': str(ticket.user.id),
                },
                receipt_email=ticket.user.email,
                description=f"Tickets for {ticket.event.title}"
            )
            
            return {
                'client_secret': intent.client_secret,
                'payment_intent_id': intent.id
            }
        except stripe.error.StripeError as e:
            # Handle Stripe-specific errors
            return {'error': str(e)}
        except Exception as e:
            # Handle other exceptions
            return {'error': 'An error occurred while processing payment.'}
    
    @staticmethod
    def confirm_payment(payment_intent_id):
        """Confirm that a payment was successful"""
        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            return {
                'status': intent.status,
                'success': intent.status == 'succeeded',
                'amount': intent.amount / 100,  # Convert back from cents
                'payment_method': intent.payment_method,
                'metadata': intent.metadata
            }
        except Exception as e:
            return {'error': str(e), 'success': False}