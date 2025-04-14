from django.urls import path
from .views import (
    OrderListCreateView,
    OrderRetrieveUpdateDestroyView,
    OrderStateUpdateView,
    OrderItemsListView,
    OrderItemCreateView,
    OrderItemDetailView
)

urlpatterns = [
    path('', OrderListCreateView.as_view(), name='order-list-create'),
    path('<int:pk>/', OrderRetrieveUpdateDestroyView.as_view(), name='order-detail'),  # Cambiado a pk
    path('<int:pk>/state/', OrderStateUpdateView.as_view(), name='order-state-update'),
    
    path('<int:order_id>/items/', OrderItemsListView.as_view(), name='order-items-list'),
    path('<int:order_id>/items/create/', OrderItemCreateView.as_view(), name='order-item-create'),
    path('<int:order_id>/items/<int:item_id>/', OrderItemDetailView.as_view(), name='order-item-detail'),
]