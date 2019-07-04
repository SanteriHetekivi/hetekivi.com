from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from . import models
from django.shortcuts import redirect
# Create your views here.


def index(request, form=None):
    models.Job.RunEncode()
    if form is None:
        form = models.Job.form()
    return HttpResponse(
        loader.get_template('encoding/index.html').render(
            {
                'encoding': models.Job.objects.order_by('id'),
                'form': form,
                'form_class': form.Meta.model.class_name(),
                'models': models,
            }, request
        )
    )


def save(request, cls, id=None):
    form = models.Base.str_class(cls).save_form(request=request)
    if(form is None):
        return redirect("index")
    else:
        return index(request, form)


def delete(request, cls, id):
    models.Base.str_class(cls).objects.filter(id=id).delete()
    return redirect("index")
