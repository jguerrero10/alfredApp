"""App configuration for the addresses application."""

from django.apps import AppConfig


class AddressesConfig(AppConfig):
    """Configuration class for the addresses app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "addresses"
