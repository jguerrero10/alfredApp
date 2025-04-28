"""Test cases for the service flow in the application."""

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from addresses.models import Address
from drivers.models import Driver
from services.models import Service

User = get_user_model()


class ServiceFlowTestCase(APITestCase):
    """Test case for the service flow in the application."""

    def setUp(self):
        """Set up the test case with necessary data."""
        self.user = User.objects.create_user(username="testuser", password="testpass123")

        self.address = Address.objects.create(street="123 Test St", city="TestCity", latitude=10.0, longitude=10.0)

        self.driver = Driver.objects.create(
            name="Test Driver", current_latitude=10.1, current_longitude=10.1, available=True
        )

        response = self.client.post(reverse("token_obtain_pair"), {"username": "testuser", "password": "testpass123"})
        self.access_token = response.data["access"]

        self.auth_headers = {"HTTP_AUTHORIZATION": f"Bearer {self.access_token}"}

    def test_request_service_assigns_driver(self):
        """Test that requesting a service assigns the nearest available driver."""
        url = reverse("service-request-service")
        data = {"client_address_id": self.address.id}
        response = self.client.post(url, data, format="json", **self.auth_headers)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        service = Service.objects.get(id=response.data["id"])
        self.assertEqual(service.driver.id, self.driver.id)
        self.assertEqual(service.status, "pending")
        self.driver.refresh_from_db()
        self.assertFalse(self.driver.available)

    def test_complete_service(self):
        """Test that completing a service marks it as completed and makes the driver available again."""
        service = Service.objects.create(
            client_address=self.address, driver=self.driver, status="pending", estimated_time_minutes=5
        )
        self.driver.available = False
        self.driver.save()

        url = reverse("service-complete-service", args=[service.id])
        response = self.client.post(url, **self.auth_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        service.refresh_from_db()
        self.assertEqual(service.status, "completed")
        self.driver.refresh_from_db()
        self.assertTrue(self.driver.available)

    def test_request_service_no_available_driver(self):
        """Test that requesting a service fails when there are no available drivers."""
        self.driver.available = False
        self.driver.save()

        url = reverse("service-request-service")
        data = {"client_address_id": self.address.id}
        response = self.client.post(url, data, format="json", **self.auth_headers)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "No available drivers at the moment.")
