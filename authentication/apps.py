from django.apps import AppConfig

# aqui  se utiliza para la configuracion de la app 

class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'# BigAutoField como tipo de campo para el identificador (ID) de los modelos en esta app
    name = 'authentication'  
      # Este es el nombre de la app que se usara en el proyecto