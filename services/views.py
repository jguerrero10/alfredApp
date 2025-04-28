"""Service ViewSet."""

from math import sqrt

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from addresses.models import Address
from drivers.models import Driver

from .models import Service
from .serializers import ServiceSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    """Viewset for the Service model."""

    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["post"], url_path="request-service")
    def request_service(self, request):
        """Endpoint to request a service and assign the nearest available driver."""
        client_address_id = request.data.get("client_address_id")

        if not client_address_id:
            return Response({"error": "client_address_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            client_address = Address.objects.get(id=client_address_id)
        except Address.DoesNotExist:
            return Response({"error": "Address does not exist."}, status=status.HTTP_404_NOT_FOUND)

        available_drivers = Driver.objects.filter(available=True)

        if not available_drivers.exists():
            return Response({"error": "No available drivers at the moment."}, status=status.HTTP_404_NOT_FOUND)

        # Calculate distance (simple Euclidean distance)
        def calculate_distance(lat1, lon1, lat2, lon2):
            return sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)

        nearest_driver = min(
            available_drivers,
            key=lambda driver: calculate_distance(
                driver.current_latitude, driver.current_longitude, client_address.latitude, client_address.longitude
            ),
        )

        # Assign driver and create service
        service = Service.objects.create(
            client_address=client_address,
            driver=nearest_driver,
            status="pending",
            estimated_time_minutes=calculate_estimated_time(nearest_driver, client_address),
        )

        # Mark driver as unavailable
        nearest_driver.available = False
        nearest_driver.save()

        serializer = self.get_serializer(service)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="complete")
    def complete_service(self, request, pk=None):
        """Endpoint to mark a service as completed."""
        try:
            service = self.get_object()
        except Service.DoesNotExist:
            return Response({"error": "Service not found."}, status=status.HTTP_404_NOT_FOUND)

        if service.status == "completed":
            return Response({"message": "Service is already completed."}, status=status.HTTP_400_BAD_REQUEST)

        # Update service status
        service.status = "completed"
        service.save()

        # Make driver available again
        if service.driver:
            service.driver.available = True
            service.driver.save()

        return Response({"message": "Service marked as completed."}, status=status.HTTP_200_OK)


def calculate_estimated_time(driver, client_address):
    """Mock function to calculate ETA. Let's assume every unit of distance equals 2 minutes."""
    distance = sqrt(
        (driver.current_latitude - client_address.latitude) ** 2
        + (driver.current_longitude - client_address.longitude) ** 2
    )
    return int(distance * 2) + 1
