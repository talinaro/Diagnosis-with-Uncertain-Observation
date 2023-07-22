from django.db import models

from .components import Component
from .io import IO
from ..utils import string_list_to_list


class Gate(models.Model):
    serial_num = models.IntegerField()
    logical_type = models.ForeignKey(Component, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    output = models.ForeignKey(IO, on_delete=models.CASCADE, related_name='output_gate')
    inputs = models.ManyToManyField(IO, related_name='input_gate')
    is_healthy = models.BooleanField(default=True)

    @property
    def op(self):
        """ Usage:
                self.op(*args) - activate the logic operation with any amount of inputs
        """
        gate_op = self.logical_type.op
        return gate_op if self.is_healthy \
            else lambda *l: not gate_op(*l)

    @classmethod
    def parse_from_file(cls, lines: list[str]):
        """ Creates a list of all the gates in the .sys files.

        Args:
            lines: list of the lines as were read from the files
                    (e.g. ['[[nand2,gate10,z1,i1,i3],', '[inverter,gate7,o1,z1]].'])

        Returns:
            list[list[str]]. List of all the separated gates descriptions as appear in the .sys files
                                (e.g. [['nand2', 'gate10', 'z1', 'i1', 'i3'],
                                       ['inverter', 'gate7', 'o1', 'z1']])
        """
        gates_lists = list(map(
            string_list_to_list,
            lines
        ))
        return gates_lists

    def calc_output(self):
        """ Calculates the output of the gate based on the provided inputs. """
        inputs = self.inputs.all()
        assert all(io.is_available() for io in inputs), \
            f'{self.name}: not all the inputs are available'

        inputs_values = [io.value for io in inputs]
        self.output.value = self.op(*inputs_values)
        self.output.save()
