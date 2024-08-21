from rest_framework.permissions import BasePermission

class IsAuthenticatedForCRUD(BasePermission):
    def has_permission(self, request, view):
        # Permettre la lecture publique pour la méthode 'list'
        if view.action == 'list':
            return True
        # Les autres actions nécessitent une authentification
        return request.user and request.user.is_authenticated
