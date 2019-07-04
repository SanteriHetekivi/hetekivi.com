from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:cls>/save', views.save, name='save_encoding'),
    path('<slug:cls>/<int:id>/delete', views.delete, name='delete_encoding'),
]
