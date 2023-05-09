from dataclasses import dataclass

from circuits_parser import Observation, Prediction, System


@dataclass
class ComparedResults:
    """ Represents couples of observation & prediction of a system for the same input values """
    observation: Observation
    prediction: Prediction


@dataclass
class Results:
    """ Represents all the observations and their predictions in a system """
    system: System
    results: list[ComparedResults]
