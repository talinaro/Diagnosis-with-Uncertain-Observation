import re

from django.db import models

from .io import IO
from .system import System
from ..utils import read_until, string_list_to_list


class Observation(models.Model):
    system = models.ForeignKey(System, on_delete=models.CASCADE, related_name='observations')
    obs_name = models.CharField(max_length=20)
    inputs = models.ManyToManyField(IO, related_name='observation_input')
    outputs = models.ManyToManyField(IO, related_name='observation_output')

    OBSERVATION_FORMAT = r'\((.+),(.+),(\[.+\])\)\.'
    IO_VALUE_FORMAT = r'(\-?)([io]\d+)'

    @classmethod
    def parse(cls, filepath):
        """ Creates the Observations from the given .obs file.

        Args:
            filepath (str): .obs file path
        """
        with open(filepath) as f:
            while obs_str := ''.join(read_until(f)):
                system_name, obs_name, io_values = re.match(cls.OBSERVATION_FORMAT, obs_str).groups()
                inputs_ios, outputs_ios = cls.__parse_io_values(io_values)
                obs = cls.objects.create(system=System.objects.get(name=system_name),
                                         obs_name=obs_name)
                obs.inputs.add(*inputs_ios)
                obs.outputs.add(*outputs_ios)

    @classmethod
    def __parse_io_values(cls, io_values: str):
        """ Creates 2 separated lists of IO inputs and IO outputs with their observed boolean values.

        Args:
            io_values: string of all the input and output values as appears in the .obs files

        Returns:
            (list[IO], list[IO]). Tuple of (list of input IOs, list of output IOs)
        """
        io_values_list: list[str] = string_list_to_list(io_values)
        inputs, outputs = [], []
        for io_val in io_values_list:
            false_sign, io_name = re.match(cls.IO_VALUE_FORMAT, io_val).groups()
            bool_val = not false_sign
            io = IO.objects.create(name=io_name, value=bool_val)
            if IO.is_input(io_name):
                inputs.append(io)
            elif IO.is_output(io_name):
                outputs.append(io)
        return inputs, outputs
