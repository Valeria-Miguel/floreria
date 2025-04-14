from .models import Flower
from users.models import CustomUser

class FlowerBuilder:
    def __init__(self):
        self.flower = Flower()
    
    def with_name(self, name):
        self.flower.name = name
        return self
    
    def with_color(self, color):
        self.flower.color = color
        return self
    
    def with_price(self, price):
        self.flower.price = price
        return self
    
    def with_stock(self, stock):
        self.flower.stock = stock
        return self
    
    def with_description(self, description):
        self.flower.description = description
        return self
    
    def with_creator(self, creator):
        if isinstance(creator, CustomUser):
            self.flower.created_by = creator
        return self
    
    def with_scent(self, has_scent=True):
        self.flower.has_scent = has_scent
        return self
    
    def with_bloom_season(self, season):
        self.flower.bloom_season = season
        return self
    
    def with_stem_length(self, length):
        self.flower.stem_length = length
        return self
    
    def with_lifespan(self, days):
        self.flower.lifespan = days
        return self
    
    def build(self):
        if not self.flower.name:
            raise ValueError("El nombre de la flor es requerido")
        if not self.flower.color:
            raise ValueError("El color de la flor es requerido")
        if not self.flower.price or self.flower.price <= 0:
            raise ValueError("El precio debe ser mayor que cero")
        
        return self.flower