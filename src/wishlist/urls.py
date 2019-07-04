from django.urls import path

from . import views
from . import models

urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:cls>/<int:id>/save', views.save, name='save'),
    path('<slug:cls>/save', views.save, name='save'),
    path('<slug:cls>/edit', views.edit, name='edit'),
    path('<slug:cls>/<int:id>/edit', views.edit, name='edit'),
    path('<slug:cls>/<int:id>/delete', views.delete, name='delete'),
]
