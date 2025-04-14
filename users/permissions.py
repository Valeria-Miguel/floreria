from rest_framework import permissions

class IsAdminOrEmpleado(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        is_admin = request.user.groups.filter(name="Administrador").exists()
        is_empleado = request.user.groups.filter(name="Empleado").exists()
        
        if is_empleado:
            return request.user.has_perm('users.change_customuser')
        return is_admin

class IsAdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.groups.filter(name="Administrador").exists()
        )

class BasePedidoPermission(permissions.BasePermission):
    """
    ayuda que solo los administradores y empleados puedan modificar pedidos
    lo s viewers solo pueden ver
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False  #bloquea a usuarios no autenticados

        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True  #todos los autenticados pueden ver

        #solo admin y empleado pueden hacer POST, PUT, DELETE
        is_admin = request.user.groups.filter(name="Administrador").exists()
        is_empleado = request.user.groups.filter(name="Empleado").exists()

        return is_admin or is_empleado

    def has_object_permission(self, request, view, obj):
        """
        verifica si el usuario tiene permisos sobre el objeto específico
        """
        is_admin = request.user.groups.filter(name="Administrador").exists()
        is_empleado = request.user.groups.filter(name="Empleado").exists()

        if request.method == "DELETE":
            # admin puede eliminar cualquier pedido, empleado solo los suyos
            return is_admin or (is_empleado and obj.usuario == request.user)

        return True  # para otros metodos, usa las reglas generales
