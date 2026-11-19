from django.db import models


class AdminUser(models.Model):
    admin_user_id = models.BigAutoField(primary_key=True)

    email = models.EmailField(
        max_length=255,
        unique=True
    )

    password_hash = models.CharField(
        max_length=255
    )

    class Meta:
        db_table = "admin_users"

    def __str__(self):
        return self.email