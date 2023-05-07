from dataclasses import dataclass

from circuits_parser import Observation, Prediction, System


@dataclass
class ComparedResults:
    observation: Observation
    prediction: Prediction


@dataclass
class Results:
    system: System
    results: list[ComparedResults]
