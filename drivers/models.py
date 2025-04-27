from django.db import models

class Driver(models.Model):
    name = models.CharField(max_length=255)
    current_latitude = models.FloatField()
    current_longitude = models.FloatField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
