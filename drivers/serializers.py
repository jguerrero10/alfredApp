"""Serializers for the Drivers application."""

from rest_framework import serializers

from .models import Driver


class DriverSerializer(serializers.ModelSerializer):
    """Serializer for the Driver model."""

    class Meta:
        """Meta class for DriverSerializer."""

        model = Driver
        fields = "__all__"
