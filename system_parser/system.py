from system_parser.gate import Gate
from system_parser.io import IO
from utils import read_clear_line, read_until


class System:
    INSTANCES = {}  # key: id, value: System

    def __init__(self, id, inputs, outputs, gates):
        self.id: str = id
        self.inputs: list[IO] = inputs
        self.outputs: list[IO] = outputs
        self.gates: list[Gate] = gates

    @classmethod
    def get(cls, id: str):
        """ Gets the System by id.

        Args:
            id (str): the id as appears in the .sys files

        Returns:
            System. Instance of cls of the provided id
                    or None if does not exist
        """
        return cls.INSTANCES.get(id, None)

    @classmethod
    def parse(cls, filepath):
        """ Creates a System from the given .sys file.

        Args:
            filepath (str): .sys file path

        Returns:
            System. New instance of cls generated from the provided args
        """
        with open(filepath) as f:
            sys_id = read_clear_line(f)[:-1]    # remove '.' at the end of id line
            inputs, outputs = IO.parse_from_file(inputs_lines=read_until(f),
                                                 outputs_lines=read_until(f))
            gates = Gate.parse_from_file(lines=read_until(f))
            return cls(id=sys_id,
                       inputs=inputs,
                       outputs=outputs,
                       gates=gates)

    def __repr__(self):
        return f'System {self.id}: ' \
               f'{len(self.inputs)} inputs, ' \
               f'{len(self.outputs)} outputs, ' \
               f'{len(self.gates)} gates'
