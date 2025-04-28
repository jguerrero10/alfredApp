"""Serializers for the addresses app."""

from rest_framework import serializers

from .models import Address


class AddressSerializer(serializers.ModelSerializer):
    """Serializer for the Address model."""

    class Meta:
        """Meta class for AddressSerializer."""

        model = Address
        fields = "__all__"
