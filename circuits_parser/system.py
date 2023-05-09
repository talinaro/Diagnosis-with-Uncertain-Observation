from circuits_parser.gate import Gate
from circuits_parser.io import IO
from utils import read_clear_line, read_until, flatten


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
            sys_id = read_clear_line(f)[:-1]  # remove '.' at the end of id line
            inputs, outputs = IO.parse_from_file(inputs_lines=read_until(f),
                                                 outputs_lines=read_until(f))
            gates = Gate.parse_from_file(lines=read_until(f))
            cls.INSTANCES[sys_id] = cls(id=sys_id,
                                        inputs=inputs,
                                        outputs=outputs,
                                        gates=gates)
            return cls.get(sys_id)

    def predict_output(self, inputs: dict[str, bool]) -> dict:
        """ Predicts the outputs the system emits for the given inputs.

        Args:
            inputs: key - input id, value - bool value

        Returns:
            dict. Dictionary of the evaluated outputs of the system in the same format as inputs
        """
        assert len(inputs) == len(self.inputs), \
            'Not all the inputs are provided to get the output prediction'

        # initialize system inputs values
        for input_obj in self.inputs:
            input_obj.value = inputs[input_obj.id]

        # propagate the inputs through the system to calculate the outputs
        for gate in self.gates:
            gate.calc_output()

        assert all(io.is_available() for io in self.outputs), \
            f'System {self.id}: could not predict all the outputs'

        outputs_dict = IO.list_to_raw_dict(ios=self.outputs)
        self.clear_ios()
        return outputs_dict

    def clear_ios(self):
        """ Clears all the IO values in the whole system (including inner gates) """
        ios = set(
            self.inputs + self.outputs +
            flatten([
                gate.inputs + [gate.output]
                for gate in self.gates
            ])
        )
        for io in ios:
            io.clear()

    def __str__(self):
        return f'System {self.id}: ' \
               f'{len(self.inputs)} inputs, ' \
               f'{len(self.outputs)} outputs, ' \
               f'{len(self.gates)} gates'
