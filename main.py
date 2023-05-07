import glob

from consts import SYS_FILE_EXTENSION, OBS_FILE_EXTENSION
from circuits_parser import parse_system, parse_observations, predict_system_output
from results import Results, ComparedResults


def main(data_systems_dir, data_observations_dir):
    # parse all the systems
    data_systems = {}  # system id -> system
    for filepath in glob.glob(pathname=fr'{data_systems_dir}/*.{SYS_FILE_EXTENSION}'):
        system = parse_system(filepath)
        data_systems[system.id] = system

    print(data_systems)

    # parse all the observations and calculate the predictions
    system_observations: dict[str, Results] = {}    # key: system id, value: observations and predictions results
    for filepath in glob.glob(pathname=fr'{data_observations_dir}/*.{OBS_FILE_EXTENSION}'):
        observations = parse_observations(filepath)
        system_id = observations[0].system_id
        system = data_systems[system_id]
        system_observations[system_id] = Results(
            system=system,
            results=[
                ComparedResults(
                    observation=obs,
                    prediction=predict_system_output(s=system, obs=obs)
                )
                for obs in observations
            ]
        )
        print(system_id, system_observations[system_id])


if __name__ == '__main__':
    main(data_systems_dir='circuits_examples/Data_Systems',
         data_observations_dir='circuits_examples/Data_Observations')
