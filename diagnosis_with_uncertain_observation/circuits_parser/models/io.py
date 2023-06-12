from django.db import models

from ..consts import INPUT_PREFIX, OUTPUT_PREFIX
from ..utils import flatten, string_list_to_list


class IO(models.Model):
    name = models.CharField(max_length=10)
    value = models.BooleanField(null=True)

    @classmethod
    def parse_from_file(cls, inputs_lines: list[str], outputs_lines: list[str]):
        """ Creates a list of all the inputs and a list of all the outputs in the .sys files.

        Args:
            inputs_lines: list of the inputs lines as were read from the files
                            (e.g. ['[i1,i2,i3,i4,i5,i6,i7,i8,', 'i9,i10,i11,i12].'])
            outputs_lines: list of the outputs lines as were read from the files
                            (e.g. ['[o1,o2].'])

        Returns:
            (list[str], list[str]). Tuple of (flattened list of all the inputs from the provided inputs lines,
                                              flattened list of all the outputs from the provided inputs lines)
        """
        inputs_names = flatten(list(map(
            string_list_to_list,
            inputs_lines
        )))
        outputs_names = flatten(list(map(
            string_list_to_list,
            outputs_lines
        )))
        return inputs_names, outputs_names

    @staticmethod
    def is_input(name: str):
        return name.startswith(INPUT_PREFIX)

    @staticmethod
    def is_output(name: str):
        return name.startswith(OUTPUT_PREFIX)

    def is_available(self):
        return self.value is not None

    def clear_value(self):
        """ Clears the value of the IO """
        self.value = None
        self.save()
