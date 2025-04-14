from rest_framework import generics
from .models import Supplier
from .serializers import SupplierSerializer
from users.permissions import IsAdminOrEmpleado, IsAdminOnly
from rest_framework.permissions import IsAuthenticated

class SupplierListView(generics.ListCreateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class SupplierDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdminOrEmpleado()]
        return super().get_permissions()