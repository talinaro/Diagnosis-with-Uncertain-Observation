import re

from django.db import models

from .gate import Gate
from .io import IO
from .system import System
from ..config import MAX_FAULTY_COMPONENTS
from ..utils import read_until, string_list_to_list, is_superset, remove_subset


class Observation(models.Model):
    system = models.ForeignKey(System, on_delete=models.CASCADE, related_name='observations')
    obs_name = models.CharField(max_length=20)
    inputs = models.ManyToManyField(IO, related_name='observation_input')
    outputs = models.ManyToManyField(IO, related_name='observation_output')

    OBSERVATION_FORMAT = r'\((.+),(.+),(\[.+\])\)\.'
    IO_VALUE_FORMAT = r'(\-?)([io]\d+)'

    @classmethod
    def parse(cls, filepath):
        """ Creates the Observations from the given .obs file.

        Args:
            filepath (str): .obs file path
        """
        with open(filepath) as f:
            while obs_str := ''.join(read_until(f)):
                system_name, obs_name, io_values = re.match(cls.OBSERVATION_FORMAT, obs_str).groups()
                inputs_ios, outputs_ios = cls.__parse_io_values(io_values)
                obs = cls.objects.create(system=System.objects.get(name=system_name),
                                         obs_name=obs_name)
                obs.inputs.add(*inputs_ios)
                obs.outputs.add(*outputs_ios)

    @classmethod
    def __parse_io_values(cls, io_values: str):
        """ Creates 2 separated lists of IO inputs and IO outputs with their observed boolean values.

        Args:
            io_values: string of all the input and output values as appears in the .obs files

        Returns:
            (list[IO], list[IO]). Tuple of (list of input IOs, list of output IOs)
        """
        io_values_list: list[str] = string_list_to_list(io_values)
        inputs, outputs = [], []
        for io_val in io_values_list:
            false_sign, io_name = re.match(cls.IO_VALUE_FORMAT, io_val).groups()
            bool_val = not false_sign
            io = IO.objects.create(name=io_name, value=bool_val)
            if IO.is_input(io_name):
                inputs.append(io)
            elif IO.is_output(io_name):
                outputs.append(io)
        return inputs, outputs

    @property
    def prediction(self):
        return self.system.predict_output(inputs=self.inputs.all())

    def find_diagnoses(self, candidates: list[list[Gate]] = None, diagnoses: tuple[list[Gate]] = ()):
        # initialize each candidate with a single gate
        if candidates is None:
            candidates = [[gate] for gate in self.system.gates.all()]
        # no more candidates, so the diagnoses are ready
        if len(candidates) == 0:
            return diagnoses

        # check whether some candidates are diagnoses
        new_diagnoses = tuple(filter(self.is_diagnosis, candidates))
        diagnoses += new_diagnoses
        # remove the new diagnoses from candidates
        remove_subset(superset=candidates, subset=new_diagnoses)

        # update the candidates by adding more gates
        new_candidates = []
        for candidate in candidates:
            optional_gates: set[Gate] = set(self.system.gates.all()) - set(candidate)
            expanded_candidate: list[list[Gate]] = [
                candidate + [gate]
                for gate in optional_gates
                if len(candidate) < MAX_FAULTY_COMPONENTS and
                   not self.is_diagnosis_superset(candidate + [gate], diagnoses)
            ]
            if expanded_candidate:
                new_candidates += expanded_candidate
        candidates = self.distinct_candidates(new_candidates)

        # recursive call
        return self.find_diagnoses(candidates, diagnoses)

    def is_diagnosis(self, candidate: list[Gate]):
        # invert the operation of the gates in the candidate
        for gate in candidate:
            gate.is_healthy = False
            gate.save()

        # predict the output of the system with this observation using the same system with inverted gates
        new_outputs = self.prediction

        # revert the system to it's original state
        for gate in candidate:
            gate.is_healthy = True
            gate.save()

        # compare this prediction with the observed output
        assert len(new_outputs) == len(self.outputs.all())
        return all(obs_output.is_member(new_outputs) for obs_output in self.outputs.all())

    @staticmethod
    def is_diagnosis_superset(candidate: list[Gate], diagnoses: list[list[Gate]]):
        return any(
            is_superset(superset=candidate, subset=diagnosis)
            for diagnosis in diagnoses
        )

    @staticmethod
    def distinct_candidates(candidates: list[list[Gate]]):
        distinct: list[list[Gate]] = []
        for candidate in candidates:
            if set(candidate) not in list(map(set, distinct)):
                distinct.append(candidate)
        return distinct
