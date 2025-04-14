from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsAdminOrEmpleado, IsAdminOnly
from .models import Order, OrderItem
from .serializers import (
    OrderSerializer,
    OrderStateUpdateSerializer,
    OrderItemSerializer
)

class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(customer=user)
    
    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

class OrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(customer=user)
    
    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAdminOnly()]
        return super().get_permissions()

class OrderStateUpdateView(generics.UpdateAPIView):
    serializer_class = OrderStateUpdateSerializer
    permission_classes = [IsAdminOrEmpleado]
    http_method_names = ['patch']
    
    def get_queryset(self):
        return Order.objects.all()
    
    def update(self, request, *args, **kwargs):
        order = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        new_state = serializer.validated_data['new_state']
        if order.change_state(new_state):
            return Response({'status': 'Estado actualizado'})
        return Response(
            {'error': 'No se pudo cambiar el estado'},
            status=status.HTTP_400_BAD_REQUEST
        )

class OrderItemsListView(generics.ListAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        order_id = self.kwargs['order_id']
        return OrderItem.objects.filter(order_id=order_id)

class OrderItemCreateView(generics.CreateAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAdminOrEmpleado]
    
    def perform_create(self, serializer):
        order_id = self.kwargs['order_id']
        order = Order.objects.get(pk=order_id)
        flower = serializer.validated_data['flower']
        serializer.save(
            order=order,
            unit_price=flower.price
        )

class OrderItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAdminOrEmpleado]
    
    def get_queryset(self):
        order_id = self.kwargs['order_id']
        return OrderItem.objects.filter(order_id=order_id)