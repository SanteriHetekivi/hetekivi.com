from django.contrib import admin
from .models import Holder, Platform, Store, Series, Type, Item

admin.site.register(Holder)
admin.site.register(Platform)
admin.site.register(Store)
admin.site.register(Series)
admin.site.register(Type)
admin.site.register(Item)
