from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    second_last_name = models.CharField(max_length=30, blank=True, null=True)
    # Additional fields can be added here

    def __str__(self):
        return self.email