""" Defines all the possible components that construct any system.

component_types: list of all those component types
"""
from typing import List


class IO:
    """ Represents a value that should be the input of the next component.

    Attributes:
        value: the binary value in any boolean representation
        next (Component): the component that gets this value as an input
                            or None if it's the system output
    """
    def __init__(self, value):
        self.value = value
        self.next: Component = None


class Component:
    """ Abstract representation of any system component. """

    def __init__(self):
        self.inputs: List[IO] = []
        self.output: IO = None

    def action(self, *inputs):
        """ Applies the action of the component on the inputs and sets the output.
        Should be OVERRIDEN by the inheriting classes.
        """
        self.inputs = inputs


class Not(Component):
    def action(self, a):
        super().action(a)
        self.output = ~a


class And(Component):
    def action(self, a, b):
        super().action(a, b)
        self.output = a & b


class Or(Component):
    def action(self, a, b):
        super().action(a, b)
        self.output = a | b


class Xor(Component):
    def action(self, a, b):
        super().action(a, b)
        self.output = a ^ b


component_types = (Not, And, Or, Xor)
