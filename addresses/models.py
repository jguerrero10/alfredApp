"""Model definition for the Address entity."""

from django.db import models


class Address(models.Model):
    """Model representing a physical address."""

    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        """Return a string representation of the address."""
        return f"{self.street}, {self.city}"
