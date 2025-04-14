from django.urls import path
from flowers.views import (
    FlowerListView, FlowerCreateView, 
    FlowerUpdateView, FlowerDeleteView
)

urlpatterns = [
    path('list/', FlowerListView.as_view(), name='flower-list'),  #solo ver
    path('create/', FlowerCreateView.as_view(), name='flower-create'),  #crear
    path('update/<int:pk>/', FlowerUpdateView.as_view(), name='flower-update'),  # modificar
    path('delete/<int:pk>/', FlowerDeleteView.as_view(), name='flower-delete'),  # eliminar
]
