from functools import reduce

from .observation import Observation
from ..config import SINGLE_OUTPUT_CERTAINTY_PROB, SINGLE_OUTPUT_UNCERTAINTY_PROB


class UncertainObservation(Observation):
    class Meta:
        proxy = True

    UNCERTAIN_OBS_NAME_PREFIX = 'u'

    @staticmethod
    def uncertain_obs_name(obs_name):
        return f'{UncertainObservation.UNCERTAIN_OBS_NAME_PREFIX}{obs_name}'

    def original_obs_name(self):
        assert self.obs_name.startswith(UncertainObservation.UNCERTAIN_OBS_NAME_PREFIX)
        return self.obs_name.lstrip(UncertainObservation.UNCERTAIN_OBS_NAME_PREFIX)

    @property
    def p(self):
        original_obs = Observation.objects.get(system=self.system, obs_name=self.original_obs_name())
        output_probs = map(
            lambda uncertain_output:
                SINGLE_OUTPUT_CERTAINTY_PROB
                if uncertain_output.value == original_obs.outputs.get(name=uncertain_output.name).value
                else SINGLE_OUTPUT_UNCERTAINTY_PROB,
            self.outputs.all()
        )
        return reduce(lambda a, b: a * b, output_probs)
