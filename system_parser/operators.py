""" Defines all possible logical operators that can appear in .sys files.

Usage:
    from operators import operators
    operators[<logical_type>]   where <logical_type> should be replaced with
                                any possible type name (such as 'and', 'xor' etc.)

Dev Usage:
    in order to add a new operator:
    * create new_op = Operator(...)
    * add new_op to `types` tuple
"""
import operator
from dataclasses import dataclass

from system_parser.consts import INVERTER, AND, OR, NAND, NOR, XOR, BUFFER


@dataclass
class Operator:
    name: str
    op: operator


Inverter = Operator(name=INVERTER, op=operator.__not__)
And = Operator(name=AND, op=operator.__and__)
Or = Operator(name=OR, op=operator.__or__)
Nand = Operator(name=NAND, op=lambda a, b: not (a and b))
Nor = Operator(name=NOR, op=lambda a, b: not (a or b))
Xor = Operator(name=XOR, op=operator.__xor__)
Buffer = Operator(name=BUFFER, op=lambda a: a)

types = (Inverter, And, Or, Nand, Nor, Xor, Buffer)
operators = {
    op_type.name: op_type
    for op_type in types
}
