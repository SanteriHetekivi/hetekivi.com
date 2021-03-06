from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from . import models
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
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


@csrf_exempt
def save(request, cls, id=None):
    form = models.EncodingBase.str_class(cls).save_form(request=request)
    if(form is None):
        return redirect("encoding_index")
    else:
        return index(request, form)


def delete(request, cls, id):
    models.EncodingBase.str_class(cls).objects.filter(id=id).delete()
    return redirect("encoding_index")


def reset(request, id):
    obj = models.Job.objects.filter(id=id)[0]
    obj.status = models.Job.WAITING
    obj.output = ""
    obj.estimate = None
    obj.last_output_time = None
    obj.save()
    return redirect("encoding_index")
