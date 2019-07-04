from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from . import models
from django.shortcuts import redirect


def index(request, form=None, form_id=None):
    if form is None:
        form = models.Item.form()
    return HttpResponse(
        loader.get_template('wishlist/index.html').render(
            {
                'wishlist': models.Item.objects.order_by('position'),
                'form': form,
                'form_id': form_id,
                'form_class': form.Meta.model.class_name(),
                'models': models,
            }, request
        )
    )


def save(request, cls, id=None):
    form = models.Base.str_class(cls).save_form(request=request, id=id)
    if(form is None):
        return redirect("index")
    else:
        return index(request, form, id)


def edit(request, cls, id=None):
    return index(request, models.Base.str_class(cls).form(id=id), id)


def delete(request, cls, id):
    models.Base.str_class(cls).objects.filter(id=id).delete()
    return redirect("index")
