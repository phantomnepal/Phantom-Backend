from rest_framework.views import APIView
from rest_framework.response import Response


from core.services.auth_service import AdminAuthService


class AdminRefreshAccessTokenView(APIView):

    def post(self, request):

        # Get refresh token from request body
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response(
                {
                    "error": "Refresh token is required"
                },
                status=400
            )

        # Generate new access token
        result, error = AdminAuthService.refresh_access_token(
            refresh_token
        )

        # Refresh token invalid/expired/revoked
        if error:
            return Response(
                {
                    "error": error
                },
                status=401
            )

        # Successfully generated new access token
        return Response(
            {
                "access_token": result["access_token"]
            },
            status=200
        )