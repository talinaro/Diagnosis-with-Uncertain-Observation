from django.db import models
from django.db.models import QuerySet, Q

from .components import Component
from .gate import Gate
from .io import IO
from ..utils import read_clear_line, read_until, clone_django_object


class System(models.Model):
    name = models.CharField(max_length=30, unique=True)
    inputs = models.ManyToManyField(IO, related_name='system_input')
    outputs = models.ManyToManyField(IO, related_name='system_output')
    gates = models.ManyToManyField(Gate, related_name='system')

    @property
    def all_ios(self):
        """ Returns all the IOs that the system has (including the inner connections between the gates). """
        return IO.objects.filter(Q(system_input=self) | Q(system_output=self) |
                                 Q(input_gate__system=self) | Q(output_gate__system=self)).distinct()

    @classmethod
    def parse(cls, filepath):
        """ Creates a System from the given .sys file.

        Args:
            filepath (str): .sys file path
        """
        with open(filepath) as f:
            sys_name = read_clear_line(f)[:-1]  # remove '.' at the end of id line
            inputs_names, outputs_names = IO.parse_from_file(inputs_lines=read_until(f),
                                                             outputs_lines=read_until(f))
            raw_gates = Gate.parse_from_file(lines=read_until(f))

        system = cls.objects.create(name=sys_name)
        system.inputs.add(*system.__create_ios(inputs_names))
        system.outputs.add(*system.__create_ios(outputs_names))
        system.__create_gates(raw_gates)

    def __create_ios(self, names: list[str]):
        """ Creates new IOs only for names that have not appear in the system till now.

        Args:
            names: list of io names

        Returns:
            list[IO]. List of the newly created IOs ONLY!
        """
        # returns a list of all the new IOs
        ios = []
        for name in names:
            io = IO.objects.filter(Q(system_input=self) | Q(system_output=self), Q(name=name))
            if not io:
                io = IO.objects.create(name=name)
                ios.append(io)
        return ios

    def __create_gates(self, raw_gates: list[list[str]]):
        """ Creates the Gates of the system from the raw data in the .sys files.

        Args:
            raw_gates: lists and strings representation of the gates as appear in the .sys files
        """
        for logical_type_name, gate_name, output_name, *inputs_names in raw_gates:
            output_io = self.all_ios.filter(name=output_name).get() \
                if self.all_ios.filter(name=output_name) \
                else IO.objects.create(name=output_name)
            gate = Gate.objects.create(
                logical_type=Component.parse(logical_type_name),
                name=gate_name,
                output=output_io
            )
            inputs = self.all_ios.filter(name__in=inputs_names)
            gate.inputs.add(*inputs)
            self.gates.add(gate)

    def predict_output(self, inputs: QuerySet):
        """ Predicts the outputs the system emits for the given inputs.

        Args:
            inputs: QuerySet of IOs

        Returns:
            list[IO]. List of IOs with the values of predicted outputs
        """
        assert inputs.count() == self.inputs.all().count(), \
            'Not all the inputs are provided to get the output prediction'

        # initialize system inputs values
        for input_obj in self.inputs.all():
            input_obj.value = inputs.get(name=input_obj.name).value
            input_obj.save()

        # propagate the inputs through the system to calculate the outputs
        for gate in self.gates.all():
            gate.calc_output()

        outputs = [
            clone_django_object(output_obj)
            for output_obj in self.outputs.all()
        ]
        assert all(io.is_available() for io in outputs), \
            f'System {self.name}: could not predict all the outputs'

        self.clear_ios()
        return outputs

    def clear_ios(self):
        """ Clears all the IO values in the whole system (including inner gates) """
        for io in self.all_ios:
            io.clear_value()
