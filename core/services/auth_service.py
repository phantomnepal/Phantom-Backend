import bcrypt
import hashlib
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from core.models.admin_users import AdminUser
from core.models.auth_refresh_token import AuthRefreshToken


class AdminAuthService:

    @staticmethod
    def admin_login(email, password):


        admin = AdminUser.objects.filter(
            email__iexact=email
        ).first()

        if not admin:
            return None, "Invalid email or password"

        stored_password = admin.password_hash

        if isinstance(stored_password, str):
            stored_password = stored_password.encode("utf-8")

        password_valid = bcrypt.checkpw(
            password.encode("utf-8"),
            stored_password
        )

        if not password_valid:
            return None, "Invalid email or password"

        refresh = RefreshToken()

        # Add your custom claims here if required
        refresh["admin_user_id"] = admin.admin_user_id

        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        refresh_expires_at = timezone.datetime.fromtimestamp(
            refresh["exp"],
            tz=timezone.get_current_timezone()
        )
        refresh_token_hash = hashlib.sha256(
            refresh_token.encode("utf-8")
        ).hexdigest()

        AuthRefreshToken.objects.create(
            token_hash=refresh_token_hash,
            user_type="admin",
            user_id=admin.admin_user_id,
            expires_at=refresh_expires_at
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "id": admin.admin_user_id,
                "email": admin.email
            }
        }, None
    

    @staticmethod
    def refresh_access_token(refresh_token_string):

        try:
            refresh_token_hash = hashlib.sha256(
                refresh_token_string.encode("utf-8")
            ).hexdigest()

            refresh = RefreshToken(refresh_token_string)
            admin_user_id = refresh["admin_user_id"]
            stored_token = AuthRefreshToken.objects.filter(
                token_hash=refresh_token_hash,
                user_type="admin",
                user_id=admin_user_id,
                expires_at__gt=timezone.now()
            ).first()
            if not stored_token:
                return None, "Refresh token is invalid or revoked"
            access_token = str(refresh.access_token)
            return {
                "access_token": access_token,
                "admin_user_id": admin_user_id
            }, None

        except TokenError:
            return None, "Invalid or expired refresh token"

        except KeyError:
            return None, "Invalid refresh token"

    @staticmethod
    def verify_refresh_token(refresh_token_string):

        try:
            # ----------------------------------
            # 1. Validate JWT itself
            # ----------------------------------
            refresh = RefreshToken(refresh_token_string)

            # ----------------------------------
            # 2. Get admin ID from custom claim
            # ----------------------------------
            admin_user_id = refresh.get("admin_user_id")

            if not admin_user_id:
                raise ValueError(
                    "Invalid refresh token"
                )

            # ----------------------------------
            # 3. Hash refresh token
            # ----------------------------------
            token_hash = hashlib.sha256(
                        refresh_token_string.encode("utf-8")
                    ).hexdigest()

            # ----------------------------------
            # 4. Check database
            # ----------------------------------
            stored_token = AuthRefreshToken.objects.filter(
                token_hash=token_hash,
                user_id=admin_user_id,
                expires_at__gt=timezone.now(),
            ).first()

            if not stored_token:
                raise ValueError(
                    "Refresh token is invalid or expired"
                )
            return True

        except (TokenError, ValueError):
            raise