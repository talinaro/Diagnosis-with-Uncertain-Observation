""" Defines all possible logical operators that can appear in .sys files.

Dev Usage:
    in order to add a new operator:
    * add it's name and operation function to the 'operators' dictionary
    * rerun migrations (remove the DB and run python manage.py migrate)
"""
import operator

from django.db import models

from ..consts import INVERTER, AND, OR, NAND, NOR, XOR, BUFFER
from ..utils import tuplize

operators = {
    INVERTER: operator.__not__,
    AND: operator.__and__,
    OR: operator.__or__,
    NAND: lambda a, b: not (a and b),
    NOR: lambda a, b: not (a or b),
    XOR: operator.__xor__,
    BUFFER: lambda a: a
}


class OperatorType(models.Model):
    name = models.CharField(max_length=30, choices=tuplize(operators.keys()), unique=True)

    @property
    def op(self):
        return operators[self.name]
