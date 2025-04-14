from rest_framework import serializers
from .models import Flower
from .builders import FlowerBuilder

class FlowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flower
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        builder = FlowerBuilder()
        
        flower = (builder
            .with_name(validated_data.get('name'))
            .with_color(validated_data.get('color'))
            .with_price(validated_data.get('price'))
            .with_stock(validated_data.get('stock', 0))
            .with_description(validated_data.get('description', ''))
            .with_creator(self.context['request'].user)
            .with_scent(validated_data.get('has_scent', False))
            .with_bloom_season(validated_data.get('bloom_season'))
            .with_stem_length(validated_data.get('stem_length'))
            .with_lifespan(validated_data.get('lifespan'))
            .build())
        
        flower.save()
        return flower