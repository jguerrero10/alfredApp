"""Serializers module for the Services application."""

from rest_framework import serializers

from .models import Service


class ServiceSerializer(serializers.ModelSerializer):
    """Serializer for the Service model."""

    class Meta:
        """Meta class for ServiceSerializer."""

        model = Service
        fields = "__all__"
        read_only_fields = ["status", "estimated_time_minutes"]
