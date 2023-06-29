""" The main functionality of the package:
    * parse_system - Parsing the system from the data .sys files and saving it in the DB
    * parse_observations - Parsing the observations from the data .obs files
"""
import pickle
import time

from django.db.models import Count

from .models import System, Observation
from .utils import mean


def parse_system(filepath):
    System.parse(filepath)


def parse_observations(filepath):
    Observation.parse(filepath)


def find_diagnosis_run_time():
    system_obs_run_times = {}
    for system in System.objects.annotate(size=Count('gates')).filter(size__lt=20).order_by('size'):
        print(f'Start running on system {system.name}')

        obs_run_times = []
        for obs in Observation.objects.filter(system=system):
            start = time.time()
            obs.find_diagnoses()
            end = time.time()
            run_time = end - start
            obs_run_times.append(run_time)
            with open(f'{system.name}.txt', 'a') as txt:
                txt.write(f'{run_time}\n')
            print(f'system {system.name}, observation {obs.obs_name}, run time: {run_time}')

        system_size = len(system.gates.all())
        if system_size not in system_obs_run_times:
            system_obs_run_times[system_size] = []
        system_obs_run_times[system_size] += obs_run_times

        with open(f'{system.name}.pickle', 'wb') as pkl:
            pickle.dump({system_size: mean(obs_run_times)}, pkl)

        print(f'{system.name} -> len {system_size}: {obs_run_times}')

    with open('bfs_run_time.pickle', 'wb') as pkl:
        pickle.dump(
            {
                system_size: mean(obs_run_times)
                for system_size, obs_run_times in system_obs_run_times.items()
            },
            pkl
        )
