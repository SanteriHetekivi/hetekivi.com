from django.db import models
import positions
from hetekivi.models import Base

# Create your models here.


class WishlistBase(Base):
    class Meta:
        abstract = True

    @staticmethod
    def model_names():
        return [
            Holder,
            Platform,
            Store,
            Series,
            Type,
            Item,
        ]


class Holder(WishlistBase):
    name = models.CharField(max_length=16)


class Platform(WishlistBase):
    holder = models.ForeignKey(
        'Holder',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=32)


class Store(WishlistBase):
    platforms = models.ManyToManyField(
        'Platform',
    )
    name = models.CharField(max_length=32)
    url = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Series(WishlistBase):
    name = models.CharField(max_length=8)


class Type(WishlistBase):
    name = models.CharField(max_length=8)


class Item(WishlistBase):
    store = models.ForeignKey(
        'Store',
        on_delete=models.PROTECT,
    )
    platform = models.ForeignKey(
        'Platform',
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
    image = models.ImageField(upload_to='wishlist/item/images/')

    def pos(self):
        return self.position+1
