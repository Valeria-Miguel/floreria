from rest_framework import serializers  
from flowers.models import Flower
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    flower = serializers.PrimaryKeyRelatedField(queryset=Flower.objects.all())
    
    class Meta:
        model = OrderItem
        fields = ['id', 'flower', 'quantity', 'unit_price', 'subtotal']
        read_only_fields = ['unit_price', 'subtotal']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    current_state_display = serializers.CharField(source='get_current_state_display', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'customer', 'created_at', 'updated_at', 
            'delivery_address', 'delivery_date', 'current_state',
            'current_state_display', 'notes', 'items', 'total_price'
        ]
        read_only_fields = ['customer', 'created_at', 'updated_at', 'total_price', 'current_state_display']

    def validate(self, data):
        items = data.get('items', [])
        flower_ids = [item['flower'].id for item in items]
        if len(flower_ids) != len(set(flower_ids)):
            raise serializers.ValidationError("No puede haber flores duplicadas en una orden")
        return data

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        
        for item_data in items_data:
            flower = item_data['flower']
            if not OrderItem.objects.filter(order=order, flower=flower).exists():
                OrderItem.objects.create(
                    order=order,
                    flower=flower,
                    quantity=item_data['quantity'],
                    unit_price=flower.price
                )
            else:
                item = OrderItem.objects.get(order=order, flower=flower)
                item.quantity += item_data['quantity']
                item.save()
        
        return order

    def update(self, instance, validated_data):
        instance.delivery_address = validated_data.get('delivery_address', instance.delivery_address)
        instance.delivery_date = validated_data.get('delivery_date', instance.delivery_date)
        instance.notes = validated_data.get('notes', instance.notes)
        instance.save()
        
        if 'items' in validated_data:
            self.update_order_items(instance, validated_data['items'])
        
        return instance
    
    def update_order_items(self, order, items_data):
        existing_items = {item.flower_id: item for item in order.items.all()}
        new_flower_ids = {item_data['flower'].id for item_data in items_data}
        
        for flower_id, item in list(existing_items.items()):
            if flower_id not in new_flower_ids:
                item.delete()
        
        for item_data in items_data:
            flower = item_data['flower']
            quantity = item_data['quantity']
            flower_id = flower.id
            
            if flower_id in existing_items:
                item = existing_items[flower_id]
                item.quantity = quantity
                item.unit_price = flower.price
                item.save()
            else:
                OrderItem.objects.create(
                    order=order,
                    flower=flower,
                    quantity=quantity,
                    unit_price=flower.price
                )

class OrderStateUpdateSerializer(serializers.Serializer):
    new_state = serializers.ChoiceField(choices=Order.STATE_CHOICES)
    
    def validate_new_state(self, value):
        order = self.context['order']
        if not order.can_change_to(value):
            raise serializers.ValidationError("Transición de estado no permitida")
        return value