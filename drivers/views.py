"""Views for the Drivers application."""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Driver
from .serializers import DriverSerializer


class DriverViewSet(viewsets.ModelViewSet):
    """Viewset for the Driver model."""

    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticated]
