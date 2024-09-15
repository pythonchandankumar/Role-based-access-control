from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        # Allow only authenticated users with the 'admin' role
        return request.user.is_authenticated and request.user.role == 'admin'
    
class IsManager(BasePermission):
    def has_permission(self, request, view):
        # Allow 'manager' to perform GET (list/retrieve), PUT (update/partial_update)
        return (request.user.is_authenticated and request.user.role == 'manager' and
                request.method in ['GET', 'PUT', 'PATCH'])

class IsSupport(BasePermission):
    def has_permission(self, request, view):
        # Allow 'supporter' to perform GET (list/retrieve) and PATCH (partial_update)
        return (request.user.is_authenticated and request.user.role == 'supporter' and
                request.method in ['GET', 'PATCH'])

class IsGuest(BasePermission):
    def has_permission(self, request, view):
        # Allow 'guest' to only perform GET (list/retrieve)
        return (request.user.is_authenticated and request.user.role == 'guest' and
                request.method in ['GET'])
