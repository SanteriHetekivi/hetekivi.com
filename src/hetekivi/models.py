from django.db import models
from django.forms.models import modelform_factory
from django.dispatch import receiver
import os


class Base(models.Model):
    isFromBase = True

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)
        self.old_file_paths = {}

    def __str__(self):
        return self.name

    @classmethod
    def form(cls, request=None, id=None):
        if request is not None and request.method == "POST":
            data = request.POST
            files = request.FILES
        else:
            data = None
            files = None
        if id is None:
            instance = None
        else:
            instance = cls.objects.get(id=id)
        return cls.form_class()(data, files, instance=instance)

    @classmethod
    def form_class(cls, id=None):
        return modelform_factory(cls, exclude=[])

    @classmethod
    def save_form(cls, request, id=None):
        if request.method != "POST":
            raise Exception(
                'Method was not POST, it was {}'.format(request.method))
        form = cls.form(request, id)
        if form.is_valid():
            form.save()
            cls.AfterSave()
            form = None
        return form

    @staticmethod
    def AfterSave():
        pass

    @classmethod
    def class_name(cls):
        return cls.__name__

    def model(self):
        return self.__class__

    def attr(self, name):
        return getattr(self, name)

    @classmethod
    def str_class(cls, class_name):
        for model in cls.__subclasses__():
            if class_name == model.class_name():
                return model
        raise Exception(
            'Class {} is not instance of {}'.format(class_name, cls.class_name()))

    @receiver(models.signals.post_delete)
    def on_post_delete(sender, instance, **kwargs):
        """Removes files after object has been saved.

        Arguments:
            sender {type} -- Model class that was deleted.
            instance {Base} -- Instance of the model that was deleted.
        """

        # Loop all fields of the intance.
        for field in instance._meta.get_fields():
            # If field is not filefield then continue.
            if not isinstance(field, models.FileField):
                continue
            try:
                # Get path of the filefield.
                file_path = instance.attr(field.name).path
                # If file exists
                if os.path.isfile(file_path):
                    # delete file.
                    instance.remove_file(field.name, file_path)
            except instance.DoesNotExist:
                continue

    @receiver(models.signals.pre_save)
    def on_pre_save(sender, instance, **kwargs):
        """Before save set old filepaths to memory.

        Arguments:
            sender {type} -- The model class that is being saved.
            instance {Base} -- Instance of the model that is being saved.
        """
        for field in instance._meta.get_fields():
            if not isinstance(field, models.FileField):
                continue
            try:
                instance.old_file_paths[field.name] = instance.model(
                ).objects.get(pk=instance.pk).attr(field.name).path
            except instance.DoesNotExist:
                continue

    @receiver(models.signals.post_save)
    def on_post_save(sender, instance, **kwargs):
        """After saving remove old files.

        Arguments:
            sender {type} -- The model class that was saved.
            instance {Base} -- Instance of the model that was saved.
        """
        for field_name, old_path in instance.old_file_paths.items():
            try:
                new_path = instance.attr(field_name).path
            except instance.DoesNotExist:
                new_path = None
            if not old_path == new_path and os.path.isfile(old_path):
                instance.remove_file(field_name, old_path)

    def remove_file(self, field_name, old_path):
        os.remove(old_path)
