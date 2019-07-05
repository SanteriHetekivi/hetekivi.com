from django.db import models
from django.core.validators import FileExtensionValidator
from django.forms.models import modelform_factory
import sys
import subprocess
import os
import threading
import re
from datetime import datetime, timedelta
from django.utils import timezone

# Create your models here.


class Base(models.Model):
    class Meta:
        abstract = True

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

    @classmethod
    def str_class(cls, classname):
        o = getattr(sys.modules[__name__], classname)
        if not issubclass(o, cls):
            raise Exception(
                'Class {} is not instance of {}'.format(classname, cls.class_name()))
        return o


class Type(Base):
    name = models.CharField(max_length=8)
    preset = models.FileField(
        validators=[
            FileExtensionValidator(['json'])
        ],
        upload_to='encoding/type/presets/'
    )


class Job(Base):
    file = models.FileField(
        validators=[
            FileExtensionValidator(['mkv'])
        ],
        upload_to='encoding/job/files/'
    )
    type = models.ForeignKey(
        'Type',
        on_delete=models.PROTECT,
    )
    output = models.CharField(max_length=128, blank=True)
    WAITING = 0
    ENCODING = 1
    DONE = 2
    STATUSES = (
        (WAITING, 'Waiting'),
        (ENCODING, 'Encoding'),
        (DONE, 'Done'),
    )
    status = models.IntegerField(choices=STATUSES, default=WAITING)
    last_output_time = models.DateTimeField(blank=True, null=True)
    estimate = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.file.name

    def filename(self):
        return os.path.basename(self.file.name)

    @classmethod
    def form_class(cls, id=None):
        return modelform_factory(cls, fields=['type', 'file'])

    def status_name(self):
        return Job.STATUSES[self.status][1]

    @staticmethod
    def AfterSave():
        Job.RunEncode()

    @staticmethod
    def RunEncode():
        thread = threading.Thread(target=Job.Encode, args=())
        thread.daemon = True
        thread.start()

    @staticmethod
    def Encode():
        if(len(Job.objects.filter(status=Job.ENCODING)) > 0):
            return
        waiting = Job.objects.filter(status=Job.WAITING)
        if len(waiting) <= 0:
            return
        waiting[0].encode()

    def encode(self):
        # Already one encoding.
        if(len(Job.objects.filter(status=Job.ENCODING)) > 0):
            return
        # Input filepath.
        input_path = self.file.path
        if not os.path.isfile(input_path):
            raise RuntimeError(
                'No input file "{}"!.'.format(
                    input_path
                )
            )
        # Output filepath.
        output_path = input_path+".tmp"
        if os.path.isfile(output_path):
            # Remove if exists.
            os.remove(output_path)
        # Preset filepath.
        preset_path = self.type.preset.path
        if not os.path.isfile(preset_path):
            raise RuntimeError(
                'No preset file "{}"!.'.format(
                    preset_path
                )
            )
        # HandBrake command.
        cmd = "HandBrakeCLI --preset-import-file '{}' -i '{}' -o '{}'".format(
            preset_path, input_path, output_path)
        print(cmd)
        # Run subprocess with command.
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True,
            universal_newlines=True
        )
        last_line = None
        return_code = None
        while True:
            # Get return code.
            return_code = process.poll()
            # If return code is given stop running.
            if return_code is not None:
                break
            # Get output line.
            line = process.stdout.readline().strip()
            print(line)
            # If line was different than last time.
            if line and line != last_line:
                last_line = line
                # Save line and info to database.
                self.output = (line[:125] + '...') if len(line) > 125 else line
                self.status = Job.ENCODING
                self.last_output_time = datetime.now(tz=timezone.utc)
                self.set_estimate(line)
                self.save()
        # If command failed.
        if return_code != 0:
            raise RuntimeError(
                'Command "{}" returned with code {}.'.format(
                    cmd, return_code
                )
            )
        # Check output file.
        if not os.path.isfile(output_path):
            raise RuntimeError(
                'No output file "{}"!.'.format(
                    output_path
                )
            )
        # Check input file
        if not os.path.isfile(input_path):
            raise RuntimeError(
                'No input file "{}"!.'.format(
                    input_path
                )
            )
        # Replace input file with output file.
        print(
            'Replacing input file "{}" with output file "{}".'.format(
                input_path,
                output_path
            )
        )
        os.replace(output_path, input_path)
        # Set status to done.
        self.status = Job.DONE
        # Emptying fields.
        self.estimate = None
        # and save object.
        print("Saving object...")
        self.save()
        # Try to start new encode.
        Job.Encode()

    def set_estimate(self, line):
        # Get hours, minutes and seconds from input.
        match = re.search(r'([0-9]*)h([0-9]*)m([0-9]*)s', line)
        # If it can't parse.
        if match is None:
            return
        # Get capture groups from the input.
        groups = match.groups()
        # If there are not exactly 3 groups.
        if len(groups) != 3:
            return
        # Make interval from the capture groups.
        interval = timedelta(
            hours=int(groups[0]),
            minutes=int(groups[1]),
            seconds=int(groups[2])
        )
        if(interval is None):
            return
        time_now = datetime.now(tz=timezone.utc)
        if(time_now is None):
            return
        complete_time = time_now + interval
        if(complete_time is None):
            return
        self.estimate = complete_time
