import bcrypt

from django.core.management.base import BaseCommand
from core.models.admin_users import AdminUser


class Command(BaseCommand):
    help = "Create the default admin user"

    def handle(self, *args, **kwargs):

        email = "admin@gmail.com"
        password = "Admin@123"

        # Check if admin already exists
        if AdminUser.objects.filter(email__iexact=email).exists():
            self.stdout.write(
                self.style.WARNING(
                    f"Admin with email {email} already exists."
                )
            )
            return

        # Hash password using bcrypt
        password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        # Create admin
        admin = AdminUser.objects.create(
            email=email,
            password_hash=password_hash
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Admin created successfully: {admin.email}"
            )
        )