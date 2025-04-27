"""Model definitions for the Drivers application."""

from django.db import models


class Driver(models.Model):
    """Model representing a driver."""

    name = models.CharField(max_length=255)
    current_latitude = models.FloatField()
    current_longitude = models.FloatField()
    available = models.BooleanField(default=True)

    def __str__(self):
        """Return a string representation of the driver."""
        return self.name
