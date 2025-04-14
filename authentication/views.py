from django.shortcuts import render #para manejar la autenticacion JWT


from rest_framework_simplejwt.views import (
    TokenObtainPairView, #obtener  los tokens
    TokenRefreshView, #refrescar el access token con un refresh token

)
