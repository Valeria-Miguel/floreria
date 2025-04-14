from django.db import models
from users.models import CustomUser

class Flower(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    has_scent = models.BooleanField(default=False)
    bloom_season = models.CharField(max_length=100, blank=True, null=True)
    stem_length = models.PositiveIntegerField(blank=True, null=True)  # en cm
    lifespan = models.PositiveIntegerField(blank=True, null=True)  # días de vida
    
    def __str__(self):
        return f"{self.name} ({self.color}) - ${self.price}"