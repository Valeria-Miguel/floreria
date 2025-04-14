from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.apps import apps
from django.core.management import call_command

@receiver(post_migrate)
def create_default_groups_and_permissions(sender, **kwargs):
    if sender.name == 'users':
        print(">>> Inicializando grupos y permisos...")
        
        try:
            UserModel = apps.get_model('users', 'CustomUser')
            content_type = ContentType.objects.get_for_model(UserModel)
            
            groups_config = {
                'Administrador': {
                    'permissions': ['add', 'change', 'delete', 'view'],
                    'description': 'Acceso completo al sistema'
                },
                'Empleado': {
                    'permissions': ['change', 'view'],
                    'description': 'Puede modificar datos pero no eliminarlos'
                },
                'Viewer': {
                    'permissions': ['view'],
                    'description': 'Solo lectura'
                }
            }
            
            for group_name, config in groups_config.items():
                group, created = Group.objects.get_or_create(
                    name=group_name,
                    defaults={'description': config['description']}
                )
                
                group.permissions.clear()
                
                for perm_prefix in config['permissions']:
                    codename = f'{perm_prefix}_customuser'
                    perm, created = Permission.objects.get_or_create(
                        codename=codename,
                        content_type=content_type,
                        defaults={'name': f'Can {perm_prefix} user'}
                    )
                    group.permissions.add(perm)
                
                print(f"Grupo {group_name} configurado con permisos: {config['permissions']}")
            
            print(">>> Grupos y permisos inicializados exitosamente")
            
        except Exception as e:
            print(f"!!! Error: {str(e)}")
            call_command('makemigrations')
            call_command('migrate')
            create_default_groups_and_permissions(sender, **kwargs)