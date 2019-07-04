import subprocess
import sys
import shlex


class Encode():

    @staticmethod
    def encode(_preset, _input, _output):
        process = subprocess.Popen(
            "HandBrakeCLI --preset-import-file '{}' -i '{}' -o '{}'".format(
                _preset, _input, _output),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True, universal_newlines=True
        )
        last_line = None
        while True:
            line = process.stdout.readline().strip()
            if line and line != last_line:
                last_line = line
                print(line)
            if process.poll() is not None:
                break
