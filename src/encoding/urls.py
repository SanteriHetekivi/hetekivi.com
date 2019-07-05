from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='encoding_index'),
    path('<slug:cls>/save', views.save, name='save_encoding'),
    path('<slug:cls>/<int:id>/delete', views.delete, name='delete_encoding'),
    path('Job/<int:id>/reset', views.reset, name='reset_job'),
]
