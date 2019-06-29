from django.db import models
import positions

# Create your models here.


class Holder(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class Platform(models.Model):
    holder = models.ForeignKey(
        'Holder',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Store(models.Model):
    platforms = models.ManyToManyField(
        'Platform',
    )
    name = models.CharField(max_length=32)
    url = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Series(models.Model):
    name = models.CharField(max_length=8)

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=8)

    def __str__(self):
        return self.name


class Item(models.Model):
    store = models.ForeignKey(
        'Store',
        on_delete=models.PROTECT,
    )
    series = models.ForeignKey(
        'Series',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    type = models.ForeignKey(
        'Type',
        on_delete=models.PROTECT,
    )
    name = models.CharField(max_length=64)
    position = positions.PositionField()
    objects = positions.PositionManager('position')
    url = models.URLField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name
