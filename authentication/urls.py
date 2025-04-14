from django.urls import path
from .views import TokenObtainPairView, TokenRefreshView # importamos las vistas para obtener y refrescar tokens

urlpatterns = [
    #ruta para obtener tokens  y refresh token ademas se  valida las credenciales del usuario y devuelve los tokens si son correctos
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  #refresh token tiene mas tiempo  y puede ser usado para obtener nuevos access tokens
]

