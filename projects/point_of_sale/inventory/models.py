from django.db import models


class ActiveManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(status=True)


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    objects = models.Manager()
    active = ActiveManager()


class UnitType(models.Model):
    short_name = models.CharField(max_length=50, unique=True)
    long_name = models.CharField(max_length=250, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.short_name


class Product(models.Model):
    code = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    name = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    price = models.PositiveBigIntegerField()
    quantity = models.FloatField()
    unit_type = models.ForeignKey(
        UnitType,
        related_name="products",
        on_delete=models.PROTECT,
    )
    image = models.ImageField(upload_to="products/%Y/%m/%d", blank=True)
    status = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + " - " + self.code

    objects = models.Manager()
    active = ActiveManager()
