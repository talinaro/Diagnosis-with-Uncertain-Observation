from django.db import models

from . import Observation


class Prediction(models.Model):
    """ Represents the predicted output that a system should emit for the inputs of the given observation. """
    observation = models.ForeignKey(Observation, on_delete=models.CASCADE, related_name='prediction')

    @property
    def outputs(self):
        return self.observation.system.predict_output(inputs=self.observation.inputs.all())
