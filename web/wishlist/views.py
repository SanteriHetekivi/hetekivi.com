from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Item
from django.shortcuts import redirect


def index(request, form=None, form_id=None):
    if form is None:
        form = Item.form()
    wishlist = Item.objects.order_by('position')
    template = loader.get_template('wishlist/index.html')
    context = {
        'wishlist': wishlist,
        'form': form,
        'form_id': form_id,
    }
    return HttpResponse(template.render(context, request))


def item_save(request, id=None):
    return save(request, Item, id)


def save(request, cls, id=None):
    return index(request, cls.save_form(request=request, id=id))


def item_edit(request, id=None):
    return edit(request, Item, id)


def edit(request, cls, id=None):
    return index(request, cls.form(id=id), id)


def item_delete(request, id):
    return delete(request, Item, id)


def delete(request, cls, id):
    cls.objects.filter(id=id).delete()
    return index(request)
