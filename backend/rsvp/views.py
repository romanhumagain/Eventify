from rest_framework import viewsets
from .models import RSVP
from .serializers import RSVPSerializer
from rest_framework.permissions import IsAuthenticated


class RSVPViewSet(viewsets.ModelViewSet):
    queryset = RSVP.objects.all()
    serializer_class = RSVPSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user) 

    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 
