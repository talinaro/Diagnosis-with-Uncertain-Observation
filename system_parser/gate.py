from system_parser.components import Component
from system_parser.io import IO
from utils import string_list_to_list


class Gate:
    def __init__(self, logical_type, id, output, inputs):
        self.logical_type: Component = logical_type
        self.id: str = id
        self.output: IO = output
        self.inputs: list[IO] = inputs

    @classmethod
    def from_list(cls, logical_type_name: str, _id: str, output_id: str, *inputs_ids):
        """ Creates a Gate from a single line of the .sys files.

        Args:
            logical_type_name: gate's name as appears in the files (e.g. 'nand2')
            _id: gate's id as appears in the files (e.g. 'gate21')
            output_id: gate's output id as appears in the files (e.g. 'o1')
            *inputs_ids: as many input ids as the gate receives (e.g. 'z15', 'i2')

        Returns:
            Gate. New instance of cls generated from the provided args
        """
        return cls(
            logical_type=Component.parse(logical_type_name),
            id=_id,
            output=IO.get(output_id),
            inputs=IO.parse_list(list(inputs_ids))
        )

    @classmethod
    def parse_from_file(cls, lines: list[str]):
        """ Creates a list of all the gates in the .sys files.

        Args:
            lines: list of the lines as were read from the files
                    (e.g. ['[[nand2,gate10,z1,i1,i3],', '[inverter,gate7,o1,z1]].'])

        Returns:
            list[Gate]. List of all the Gate instances generated from the provided lines
        """
        gates_lists = list(map(
            string_list_to_list,
            lines
        ))
        return [cls.from_list(*gate_params) for gate_params in gates_lists if len(gate_params) >= 4]
