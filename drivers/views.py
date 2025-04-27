from rest_framework import viewsets
from .models import Driver
from .serializers import DriverSerializer
from rest_framework.permissions import IsAuthenticated

class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticated]
