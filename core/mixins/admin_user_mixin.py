from core.models.admin_users import AdminUser
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response


class AdminUserMixin:
    """
    Mixin to extract admin user from JWT token
    """
    
    def get_admin_user(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None, Response({"error": "No token"}, status=400)

        token = auth_header.split(" ")[1]

        try:
            decoded = AccessToken(token)
        except Exception as e:
            return None, Response({"error": "Invalid token or expired token"}, status=401)

        user_id = decoded.get("admin_user_id") 

        if not user_id:
            return None, Response({"error": "Invalid token"}, status=400)

        admin_user = AdminUser.objects.filter(admin_user_id=user_id).first()

        if not admin_user:
            return None, Response({"error": "User not found"}, status=400)

        return admin_user, None 
    
    def get_user_or_error(self, request):
        """
        Returns admin user or raises exception with error response
        """
        user, error_response = self.get_admin_user(request)
        if error_response:
            return None, error_response
        return user, None
