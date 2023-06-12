import re
from functools import reduce

from django.db import models

from .operators import OperatorType


class Component(models.Model):
    """ Represents any logic type of a gate as appears in the .sys files.

    Usage:
        self.op(*args) - activate the logic operation with any amount of inputs
    """
    operator_type = models.ForeignKey(OperatorType, on_delete=models.CASCADE)
    inputs_num = models.PositiveSmallIntegerField(default=1)

    NAME_FORMAT = r'(\D+)(\d*)'

    @property
    def op(self):
        return self.operator_type.op if self.inputs_num == 1 \
            else lambda *l: reduce(self.operator_type.op, l)

    @classmethod
    def parse(cls, name):
        """ Creates a Component from it's name.

        Args:
            name (str): full logic type as appears in .sys files

        Returns:
            Component. New instance of cls generated from the provided args
        """
        op_name, inputs_num_str = re.match(cls.NAME_FORMAT, name).groups()

        inputs_num = int(inputs_num_str) if inputs_num_str \
            else cls._meta.get_field('inputs_num').get_default()

        obj, _ = cls.objects.get_or_create(
            operator_type=OperatorType.objects.get(name=op_name),
            inputs_num=inputs_num
        )
        return obj
