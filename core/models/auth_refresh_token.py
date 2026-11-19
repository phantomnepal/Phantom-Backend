from django.db import models


class AuthRefreshToken(models.Model):
    auth_refresh_token_id = models.BigAutoField(primary_key=True)

    token_hash = models.CharField(
        max_length=64,
        unique=True
    )

    user_type = models.CharField(
        max_length=50
    )

    user_id = models.BigIntegerField()

    expires_at = models.DateTimeField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "auth_refresh_tokens"

    def __str__(self):
        return f"{self.user_type} - {self.user_id}"