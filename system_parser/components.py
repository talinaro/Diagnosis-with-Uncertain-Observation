import re

from system_parser.operators import Operator, operators


class Component:
    """ Represents any logic type of a gate as appears in the .sys files.

    Attributes:
        self.operation (Operator): logic operation of the component
        self.inputs_num (int): number of inputs the component receives
    """
    NAME_FORMAT = r'(\D+)(\d*)'

    def __init__(self, operation, inputs_num=1):
        self.operation: Operator = operation
        self.inputs_num: int = inputs_num

    @classmethod
    def parse(cls, name):
        """ Creates a Component from it's name.

        Args:
            name (str): full logic type as appears in .sys files

        Returns:
            Component. New instance of cls generated from the provided args
        """
        op_name, inputs_num_str = re.match(cls.NAME_FORMAT, name).groups()

        assert op_name in operators, \
            f'No such component {op_name}'

        component = cls(operation=operators[op_name])
        if inputs_num_str:
            component.inputs_num = int(inputs_num_str)
        return component
