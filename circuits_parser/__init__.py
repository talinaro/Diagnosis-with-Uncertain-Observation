""" The main functionality of the package:
    * parse_system - Parsing the system from the data .sys files
    * parse_observations - Parsing the observations from the data .obs files
    * predict_system_output - Predicting the output a system should get for the input of the provided observation
"""
from circuits_parser.observation import Observation
from circuits_parser.prediction import Prediction
from circuits_parser.system import System


def parse_system(filepath) -> System:
    return System.parse(filepath)


def parse_observations(filepath) -> list[Observation]:
    return Observation.parse(filepath)


def predict_system_output(s: System, obs: Observation):
    return Prediction(system=s, inputs=obs.inputs_values)
