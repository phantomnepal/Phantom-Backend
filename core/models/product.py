from django.db import models


class Product(models.Model):

    class StockStatus(models.TextChoices):
        IN_STOCK = "IN_STOCK", "In Stock"
        LIMITED = "LIMITED", "Limited Stock"
        OUT_OF_STOCK = "OUT_OF_STOCK", "Out of Stock"

    name = models.CharField(
        max_length=200
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    small_description = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    long_description = models.TextField(
        blank=True,
        null=True
    )

    category = models.CharField(
        max_length=100,
        db_index=True,
        null=True,
        blank=True
    )

    quantity = models.PositiveIntegerField(
        default=0
    )

    stock_status = models.CharField(
        max_length=20,
        choices=StockStatus.choices,
        default=StockStatus.IN_STOCK
    )

    limited_stock_status = models.BooleanField(
        default=False
    )

    image = models.URLField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        null=True,
        blank=True
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["category"]),
            models.Index(fields=["stock_status"]),
        ]

    def __str__(self):
        return self.name