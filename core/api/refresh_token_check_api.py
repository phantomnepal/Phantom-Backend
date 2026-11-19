from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.services.auth_service import AdminAuthService


class AdminAuthCheckView(APIView):

    def get(self, request):

        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response(
                {"authenticated": False},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:

            AdminAuthService.verify_refresh_token(
                refresh_token
            )

            return Response(
                {"authenticated": True},
                status=200
            )

        except Exception  as e:
            return Response(
                {"authenticated": False},
                status=400
            )