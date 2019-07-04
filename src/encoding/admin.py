from django.contrib import admin

# Register your models here.
from .models import Type, Job

admin.site.register(Type)
admin.site.register(Job)
