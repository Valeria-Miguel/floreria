from django.urls import path
from .views import SupplierListView, SupplierDetailView

urlpatterns = [
    path('', SupplierListView.as_view(), name='supplier-list'),
    path('<int:pk>/', SupplierDetailView.as_view(), name='supplier-detail'),
]