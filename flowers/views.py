from rest_framework import generics
from .models import Flower
from .serializers import FlowerSerializer
from users.permissions import IsAdminOrEmpleado, IsAdminOnly
from rest_framework.permissions import IsAuthenticated

class FlowerListView(generics.ListAPIView):
    queryset = Flower.objects.all()
    serializer_class = FlowerSerializer
    permission_classes = [IsAuthenticated]

class FlowerCreateView(generics.CreateAPIView):
    queryset = Flower.objects.all()
    serializer_class = FlowerSerializer
    permission_classes = [IsAdminOrEmpleado]

class FlowerUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Flower.objects.all()
    serializer_class = FlowerSerializer
    permission_classes = [IsAdminOrEmpleado]

class FlowerDeleteView(generics.DestroyAPIView):
    queryset = Flower.objects.all()
    serializer_class = FlowerSerializer
    permission_classes = [IsAdminOnly]

    ##patrones que puedp usar 
  #  state para las ordenes en el estado de pendente realizadoo hacer yy asi ---- en ordenes 
   # tambien el observer rn ordenes para actualizar el inventario---- en orden
     # Singleton Pattern
#Si usas un servicio que se debe compartir globalmente (por ejemplo, un StockManager que actualiza stock en varias apps).
        