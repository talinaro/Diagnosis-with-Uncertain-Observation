from django.db import models

from .gate import Gate
from .observation import Observation


class Diagnosis(models.Model):
    observation = models.ForeignKey(Observation, on_delete=models.CASCADE, related_name='diagnosis')
    invalid_gates = models.ManyToManyField(Gate)

    @staticmethod
    def save_diagnoses(observation: Observation, diagnoses: list[list[Gate]]):
        for diagnosis_gates in diagnoses:
            diagnosis_obj = Diagnosis.objects.create(observation=observation)
            diagnosis_obj.invalid_gates.add(*diagnosis_gates)

    def __eq__(self, other):
        return self.observation.system == other.observation.system and \
            set(self.invalid_gates) == set(other.invalid_gates)
