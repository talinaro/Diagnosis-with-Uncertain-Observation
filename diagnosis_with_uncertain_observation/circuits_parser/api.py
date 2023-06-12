""" The main functionality of the package:
    * parse_system - Parsing the system from the data .sys files and saving it in the DB
    * parse_observations - Parsing the observations from the data .obs files
    * predict_system_output - Predicting the output a system should get for the input of the provided observation
"""
from .models import System, Observation, Prediction


def parse_system(filepath):
    System.parse(filepath)


def parse_observations(filepath):
    Observation.parse(filepath)


def predict_output(observation: Observation):
    # return Prediction.objects.create(system=obs.system,
    #                                  inputs=obs.inputs)
    return Prediction.objects.create(observation=observation)
