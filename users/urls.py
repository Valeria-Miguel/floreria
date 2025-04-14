from django.urls import path, include 
from .views import RegisterView, UserViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'users', UserViewSet)  


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register-user'),
    path('', include(router.urls)),  
]