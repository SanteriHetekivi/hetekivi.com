from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Item
from .forms import ItemForm
from django.shortcuts import redirect


def index(request, id=None):
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            form = ItemForm()
    else:
        form = ItemForm()
    wishlist = Item.objects.order_by('position')
    template = loader.get_template('wishlist/index.html')
    context = {
        'wishlist': wishlist,
        'form': form,
    }
    return HttpResponse(template.render(context, request))


def delete(request, id):
    Item.objects.filter(id=id).delete()
    return redirect('/wishlist')
