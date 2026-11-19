
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.services.auth_service import AdminAuthService


class AdminLoginAPIView(APIView):

    def post(self, request):

        email = request.data.get("email")
        password = request.data.get("password")

        # Validate input
        if not email or not password:
            return Response(
                {
                    "status": "error",
                    "message": "Email and password are required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Authenticate user
        result, error = AdminAuthService.admin_login(
            email=email,
            password=password
        )

        if error:
            return Response(
                {
                    "status": "error",
                    "message": error
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Return both tokens to Next.js BFF
        return Response(
            {
                "status": "success",
                "data": {
                    "access_token": result["access_token"],
                    "refresh_token": result["refresh_token"],
                    "user": result["user"]
                }
            },
            status=status.HTTP_200_OK
        )
