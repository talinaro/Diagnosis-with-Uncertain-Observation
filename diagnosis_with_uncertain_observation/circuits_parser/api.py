import operator
import pickle
import time
from functools import reduce

from django.db.models import Count

from .config import RESULTS_RUN_TIMES_DIR, RESULTS_DIAGNOSIS_PROBABILITIES_DIR
from .models import System, Observation, Diagnosis, UncertainObservation, IO
from .utils import mean, num_to_booleans


def parse_system(filepath):
    System.parse(filepath)


def parse_observations(filepath):
    Observation.parse(filepath)


def find_diagnosis():
    """ Looks for diagnoses of all the uncertain observations of all the systems and saves them in the DB.
    Meanwhile, calculates the run time of the algorithm on each observation and stores the results in files.
    """
    system_obs_run_times = {}
    for system in System.objects.annotate(size=Count('gates')).order_by('size'):
        print(f'Start running on system {system.name}')

        # find diagnoses from all uncertain observations of the system
        obs_run_times = []
        for obs in Observation.objects.filter(system=system):
            for uncertain_obs in create_uncertain_observations(observation=obs):
                start = time.time()
                diagnoses = uncertain_obs.find_diagnoses()
                end = time.time()
                run_time = end - start
                obs_run_times.append(run_time)
                # save each observation BFS run time in file
                with open(f'{RESULTS_RUN_TIMES_DIR}/{system.name}.txt', 'a') as txt:
                    txt.write(f'{run_time}\n')
                print(f'system {system.name}, observation {uncertain_obs.obs_name}, run time: {run_time}')
                # save all the diagnoses gotten form BFS on observation to DB
                Diagnosis.save_diagnoses(uncertain_observation=uncertain_obs, diagnoses=diagnoses)

        save_txt_results(system.name)

        system_size = len(system.gates.all())
        if system_size not in system_obs_run_times:
            system_obs_run_times[system_size] = []
        system_obs_run_times[system_size] += obs_run_times

        print(f'{system.name} -> len {system_size}: {mean(obs_run_times)}')

    with open(f'{RESULTS_RUN_TIMES_DIR}/bfs_run_time.pickle', 'wb') as pkl:
        pickle.dump(
            {
                system_size: mean(obs_run_times)
                for system_size, obs_run_times in system_obs_run_times.items()
            },
            pkl
        )


def top_diagnoses(system_name, n=None) -> list[tuple[list[str], float]]:
    """ Returns the n most probable diagnoses of the given system where each diagnosis represented as a list of gates.
    If no n provided, returns all the diagnoses in descending probability order.

    E.g., for n=4: [(['gate10'], 0.179),
                    (['gate18'], 0.140),
                    (['gate14', 'gate21'], 0.127),
                    (['gate11', 'gate17', 'gate21'], 0.0008)]
    """
    all_system_diagnoses = Diagnosis.objects.filter(uncertain_observation__system__name=system_name)
    n = all_system_diagnoses.count() if n is None else n

    system_diagnoses_prob = diagnoses_probs(system_name)

    return list(map(
        lambda diag_prob: (diag_prob[0].invalid_gates_names(), diag_prob[1]),
        sorted(system_diagnoses_prob.items(), key=operator.itemgetter(1), reverse=True)[:n]
    ))


def create_uncertain_observations(observation: Observation):
    obs_outputs = observation.outputs.order_by('name')
    output_combinations_num = 2 ** len(obs_outputs)
    for combination_i in range(output_combinations_num):
        bool_values = num_to_booleans(num=combination_i, length=len(obs_outputs))
        # create new uncertain observation object
        uncertain_obs = UncertainObservation.objects.create(
            system=observation.system,
            obs_name=UncertainObservation.uncertain_obs_name(observation.obs_name)
        )
        uncertain_obs.inputs.add(*observation.inputs.all())
        uncertain_obs.outputs.add(*[
            IO.objects.create(name=io.name, value=new_value)
            for (io, new_value) in zip(obs_outputs, bool_values)
        ])
        yield uncertain_obs


def diagnoses_probs(system_name) -> dict[Diagnosis: float]:
    """ Find all similar diagnoses in the same system and calculate the total probability of each """
    system_diagnoses_prob = {}  # key: Diagnosis, value: probability
    for diagnosis in Diagnosis.objects.filter(uncertain_observation__system__name=system_name):
        if diagnosis in list(system_diagnoses_prob.keys()):
            continue
        similar_diagnosis_probs = map(lambda d: d.p, diagnosis.all_similar_diagnoses())
        total_diagnosis_prob = reduce(lambda p1, p2: p1 + p2, similar_diagnosis_probs)
        system_diagnoses_prob[diagnosis] = total_diagnosis_prob
    return system_diagnoses_prob


def save_txt_results(system_name):
    """ Saves the diagnoses of the system in descending probability order in a file """
    diagnoses_prob: list[tuple[list[str], float]] = top_diagnoses(system_name)
    with open(f'{RESULTS_DIAGNOSIS_PROBABILITIES_DIR}/{system_name}_1.0.txt', 'a') as txt:
        for diagnosis, p in diagnoses_prob:
            txt.write(f'{diagnosis}: p = {p}\n')
