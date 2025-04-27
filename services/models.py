"""Models module for the Services application."""

from django.db import models

from addresses.models import Address
from drivers.models import Driver


class Service(models.Model):
    """Model representing a service request."""

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
    ]

    client_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    estimated_time_minutes = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the service."""
        return f"Service #{self.pk} - {self.status}"
