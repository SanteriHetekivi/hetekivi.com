from django.db import models
import positions
from django.forms.models import modelform_factory

# Create your models here.


class Base(models.Model):
    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    @classmethod
    def form(cls, request=None, id=None):
        if request is not None and request.method == "POST":
            data = request.POST
        else:
            data = None
        if id is None:
            instance = None
        else:
            instance = cls.objects.get(id=id)
        return cls.form_class()(data, instance=instance)

    @classmethod
    def form_class(cls, id=None):
        return modelform_factory(cls, exclude=[])

    @classmethod
    def save_form(cls, request, id=None):
        if request.method != "POST":
            raise Exception(
                'Method was not POST, it was {}'.format(request.method))
        form = cls.form(request, id)
        if form.is_valid():
            form.save()
            form = cls.form()
        return form


class Holder(Base):
    name = models.CharField(max_length=16)


class Platform(Base):
    holder = models.ForeignKey(
        'Holder',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=32)


class Store(Base):
    platforms = models.ManyToManyField(
        'Platform',
    )
    name = models.CharField(max_length=32)
    url = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Series(Base):
    name = models.CharField(max_length=8)


class Type(Base):
    name = models.CharField(max_length=8)


class Item(Base):
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
