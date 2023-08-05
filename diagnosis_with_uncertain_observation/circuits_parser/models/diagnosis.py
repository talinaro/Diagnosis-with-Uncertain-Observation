from django.db import models

from .uncertain_observation import UncertainObservation
from .gate import Gate
from ..config import SINGLE_GATE_FAULTY_PROB


class Diagnosis(models.Model):
    uncertain_observation = models.ForeignKey(UncertainObservation, on_delete=models.CASCADE, related_name='diagnosis')
    invalid_gates = models.ManyToManyField(Gate)

    @staticmethod
    def save_diagnoses(uncertain_observation: UncertainObservation, diagnoses: tuple[list[Gate]]):
        for diagnosis_gates in diagnoses:
            diagnosis_obj = Diagnosis.objects.create(uncertain_observation=uncertain_observation)
            diagnosis_obj.invalid_gates.add(*diagnosis_gates)

    @property
    def p(self):
        return (SINGLE_GATE_FAULTY_PROB ** self.invalid_gates.count()) * self.uncertain_observation.p

    def all_similar_diagnoses(self):
        """ Returns all the diagnoses that similar to this one """
        return filter(lambda d: d == self,
                      Diagnosis.objects.filter(uncertain_observation__system=self.uncertain_observation.system))

    def invalid_gates_names(self):
        return list(map(lambda gate: gate.name, self.invalid_gates.all()))

    def __eq__(self, other):
        # diagnoses are equal if they relate to the same system and have the same set of invalid gates
        return self.uncertain_observation.system == other.uncertain_observation.system and \
            set(self.invalid_gates.all()) == set(other.invalid_gates.all())

    def __hash__(self):
        return hash((self.uncertain_observation.system, self.invalid_gates))
