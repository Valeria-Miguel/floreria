from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.models import Group

class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    update_role = serializers.CharField(
        write_only=True,
        required=False,
        allow_null=True,
        allow_blank=True,
        error_messages={
            'invalid_choice': 'Rol no válido. Opciones: Administrador, Empleado, Viewer'
        }
    )

    def get_role(self, obj):
        return obj.groups.first().name if obj.groups.exists() else None

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'second_last_name', 'role', 'update_role']
        extra_kwargs = {
            'username': {'read_only': True}
        }

    def validate(self, data):
        errors = {}
        
        if 'update_role' in data and data['update_role']:
            data['update_role'] = str(data['update_role']).strip('"')
            if data['update_role'] not in ['Administrador', 'Empleado', 'Viewer']:
                errors['update_role'] = f"'{data['update_role']}' no es una opción válida. Opciones: Administrador, Empleado, Viewer"
        
        if 'first_name' in data and not data['first_name']:
            errors['first_name'] = "El campo first_name no puede estar vacío."
        if 'last_name' in data and not data['last_name']:
            errors['last_name'] = "El campo last_name no puede estar vacío."
        
        if errors:
            raise serializers.ValidationError(errors)
        return data

    def update(self, instance, validated_data):
        new_role = validated_data.pop('update_role', None)
        
        if new_role:
            instance.groups.clear()
            try:
                group = Group.objects.get(name=new_role)
                instance.groups.add(group)
            except Group.DoesNotExist:
                raise serializers.ValidationError(
                    {'update_role': f"El grupo '{new_role}' no existe. Contacte al administrador."}
                )
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
    

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(
        choices=['Administrador', 'Empleado', 'Viewer'],
        required=True,
        write_only=True,  
        allow_blank=False,
        error_messages={
            'required': 'El campo rol es obligatorio',
            'invalid_choice': 'Rol no válido. Opciones: Administrador, Empleado, Viewer'
        }
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'second_last_name', 'role']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, data):
        errors = {}
        if 'role' not in data or not data['role']:
            errors['role'] = "El campo rol es obligatorio."
        else:
            data['role'] = str(data['role']).strip('"')
            if data['role'] not in ['Administrador', 'Empleado', 'Viewer']:
                errors['role'] = f"'{data['role']}' no es una opción válida. Opciones: Administrador, Empleado, Viewer"
        if 'first_name' not in data or not data['first_name']:
            errors['first_name'] = "El campo first_name es obligatorio."
        if 'last_name' not in data or not data['last_name']:
            errors['last_name'] = "El campo last_name es obligatorio."
        
        if errors:
            raise serializers.ValidationError(errors)
        return data

    def create(self, validated_data):
        role = validated_data.pop('role')
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            second_last_name=validated_data.get('second_last_name', '')
        )
        try:
            group = Group.objects.get(name=role)
            user.groups.add(group)
            print(f"Usuario {user.username} asignado al grupo {group.name}")
        except Group.DoesNotExist:
            print(f"Error: El grupo '{role}' no existe.")
            raise serializers.ValidationError(
                f"El grupo '{role}' no existe. Contacte al administrador."
            )
        return user

    def to_representation(self, instance):
        return {
            'username': instance.username,
            'email': instance.email,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'second_last_name': instance.second_last_name,
            'message': 'Usuario registrado exitosamente'
        }