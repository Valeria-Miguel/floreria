from rest_framework import serializers
from .models import Supplier

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = [
            'id', 'name', 'contact_person', 'email', 
            'phone', 'address', 'tax_id', 'notes',
            'created_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']
    
    def validate_tax_id(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("El tax ID debe tener al menos 5 caracteres")
        return value