from django.db import models
from django.core.validators import MinValueValidator
from flowers.models import Flower
from users.models import CustomUser

class Order(models.Model):
    STATE_CHOICES = (
        ('PENDING', 'Pendiente'),
        ('PREPARING', 'En preparación'),
        ('READY', 'Lista para entregar'),
        ('DELIVERED', 'Entregada'),
        ('CANCELLED', 'Cancelada')
    )
    
    customer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    delivery_address = models.TextField()
    delivery_date = models.DateTimeField()
    current_state = models.CharField(max_length=20, choices=STATE_CHOICES, default='PENDING')
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Orden #{self.id} - {self.get_current_state_display()}"
    
    def can_change_to(self, new_state):
        transitions = {
            'PENDING': ['PREPARING', 'CANCELLED'],
            'PREPARING': ['READY', 'CANCELLED'],
            'READY': ['DELIVERED', 'CANCELLED'],
            'DELIVERED': [],
            'CANCELLED': []
        }
        return new_state in transitions.get(self.current_state, [])
    
    def change_state(self, new_state):
        if self.can_change_to(new_state):
            self.current_state = new_state
            self.save()
            return True
        return False
    
    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    flower = models.ForeignKey(Flower, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        unique_together = ('order', 'flower')
    
    @property
    def subtotal(self):
        return self.unit_price * self.quantity
    
    def __str__(self):
        return f"{self.quantity} x {self.flower.name} (${self.subtotal})"