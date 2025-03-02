from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import TicketSerializer
from events.models import Event
from rest_framework import status
from rest_framework.views import APIView
from.models import Ticket

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


  