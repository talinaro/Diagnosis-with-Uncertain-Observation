from circuits_parser.consts import INPUT_PREFIX, OUTPUT_PREFIX
from utils import flatten, string_list_to_list


class IO:
    """ Represents an input/output in a system.

    Notes:
        The CACHE is here for internal usage only!!!
        It actually saves all the IOs that had been already created while a system generation,
        and got cleared before any new system generation.

        DO NOT use the get() method not while system generation!
    """
    CACHE = {}  # key: id, value: IO

    def __init__(self, id, value=None):
        self.id: str = id
        self.value: bool = value

    @classmethod
    def get(cls, id: str):
        """ Creates an IO from it's id
            or returns it from the cache if were previously created.

            NOTE: Usage is available ONLY while system generation!!!

        Args:
            id (str): the id as appears in the .sys files

        Returns:
            IO. Instance of cls generated from the provided args
        """
        if id not in cls.CACHE:
            cls.CACHE[id] = cls(id=id)
        return cls.CACHE[id]

    @classmethod
    def parse_list(cls, ids: list[str]):
        """ Creates a list of IOs of the given ids.

        Args:
            ids: list of ids

        Returns:
            list[IO]. List of all the IO instances generated from the provided ids
        """
        return [cls.get(id=id) for id in ids]

    @classmethod
    def parse_from_file(cls, inputs_lines: list[str], outputs_lines: list[str]):
        """ Creates a list of all the inputs and a list of all the outputs in the .sys files.

        Args:
            inputs_lines: list of the inputs lines as were read from the files
                            (e.g. ['[i1,i2,i3,i4,i5,i6,i7,i8,', 'i9,i10,i11,i12].'])
            outputs_lines: list of the outputs lines as were read from the files
                            (e.g. ['[o1,o2].'])

        Returns:
            (list[IO], list[IO]). Tuple of (list of all the IO instances generated from the provided inputs lines,
                                            list of all the IO instances generated from the provided outputs lines)
        """
        cls.__clear_cache()     # parsing from new file, so its a new system with other ios
        inputs_ids = flatten(list(map(
            string_list_to_list,
            inputs_lines
        )))
        outputs_ids = flatten(list(map(
            string_list_to_list,
            outputs_lines
        )))
        return cls.parse_list(inputs_ids), cls.parse_list(outputs_ids)

    @classmethod
    def __clear_cache(cls):
        cls.CACHE = {}

    @staticmethod
    def is_input(id: str):
        return id.startswith(INPUT_PREFIX)

    @staticmethod
    def is_output(id: str):
        return id.startswith(OUTPUT_PREFIX)

    def is_available(self):
        return self.value is not None

    @staticmethod
    def list_to_raw_dict(ios):
        """ Converts a list of IOs into simple dictionary of ids and values.
        E.g.:
            [IO(id='i1', value=True), IO(id='i2', value=False)]
                -> { 'i1': True, 'i2': False }

        Args:
            ios (list): list of IO instances

        Returns:
            Dict. Generated dictionary from the given list when:  key: io id
                                                                  value: io bool value
        """
        return {
            io.id: io.value
            for io in ios
        }

    def clear(self):
        """ Clears the value of the IO """
        self.value = None

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f'{self.id}={self.value}'
