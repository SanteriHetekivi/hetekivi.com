from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Item/<int:id>/delete', views.item_delete, name='item_delete'),
    path('Item/<int:id>/edit', views.item_edit, name='item_edit'),
    path('Item/<int:id>/save', views.item_save, name='item_save'),
    path('Item/save', views.item_save, name='item_save'),
]
