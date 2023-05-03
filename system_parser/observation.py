import re

from system_parser.io import IO
from utils import read_until, string_list_to_list


class Observation:
    OBSERVATION_FORMAT = r'\((.+),(.+),(\[.+\])\)\.'
    IO_VALUE_FORMAT = r'(\-?)([io]\d+)'

    def __init__(self, system_id, obs_id, inputs_values, outputs_values):
        self.system_id: str = system_id
        self.obs_id: str = obs_id
        self.inputs_values: dict = inputs_values  # key: i_id, value: bool
        self.outputs_values: dict = outputs_values  # key: o_id, value: bool

    @classmethod
    def parse(cls, filepath):
        """ Creates a list of Observations from the given .obs file.

        Args:
            filepath (str): .obs file path

        Yields:
            list[Observation]. List of new instances of cls generated from the provided args
        """
        with open(filepath) as f:
            observations = []
            while obs_str := ''.join(read_until(f)):
                system_id, obs_id, io_values = re.match(cls.OBSERVATION_FORMAT, obs_str).groups()
                inputs_values, outputs_values = cls.__parse_io_values(io_values)
                observations.append(cls(system_id=system_id,
                                        obs_id=obs_id,
                                        inputs_values=inputs_values,
                                        outputs_values=outputs_values))
            return observations

    @classmethod
    def __parse_io_values(cls, io_values: str):
        """ Retrieves the boolean values of the observation
        into separate dictionaries for inputs and outputs.

        Args:
            io_values: string of all the input and output values as appears in the .obs files

        Returns:
            (dict, dict). Tuple of (inputs dictionary, output dictionary)
                          when each dict in the format of:  key: io id (e.g. 'i1', 'o3')
                                                            value: bool value provided by the observation
        """
        io_values_list: list[str] = string_list_to_list(io_values)
        inputs, outputs = {}, {}
        for io_val in io_values_list:
            false_sign, io_id = re.match(cls.IO_VALUE_FORMAT, io_val).groups()
            bool_val = not false_sign
            if IO.is_input(io_id):
                inputs[io_id] = bool_val
            elif IO.is_output(io_id):
                outputs[io_id] = bool_val
        return inputs, outputs
