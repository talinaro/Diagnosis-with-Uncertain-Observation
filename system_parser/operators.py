import operator
from dataclasses import dataclass


@dataclass
class Operator:
    op: operator


Inverter = Operator(op=operator.__not__)
And = Operator(op=operator.__and__)
Or = Operator(op=operator.__or__)
Nand = Operator(op=lambda a, b: not (a and b))
Nor = Operator(op=lambda a, b: not (a or b))
Xor = Operator(op=operator.__xor__)
Buffer = Operator(op=lambda a: a)
