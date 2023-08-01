# Diagnosis-with-Uncertain-Observation

## Description
In anomaly detection, uncertainty over the observations can happen when a noisy sensor is used to collect the output.
We would like to take in consideration the fact that the observations can be mistaken with some probability in order to, hopefully, provide more accurate and reliable fault diagnosis.


## Data
The data consists of `txt` files of system descriptions and observations.
Each system has a single description file `.sys` and a single `.obs` file (with corresponding name) of multiple observations propagated through the system.
Examples of those files are available in `circuits_examples\` directory.


## Implementation
The project implemented using [Django Framework](https://docs.djangoproject.com/en/4.2/) for modeling the various object types and storing them in the DB.

At first, the systems and the observations should be parsed from the `txt` data files and stored as model instances in the DB. 
It should be done only once at the beginning, especially that most of the systems are heavy (it takes a few minutes to parse all the data).

Then, the diagnosis searching algorithm runs (based on [O2D (Observations to Diagnoses)](https://ojs.aaai.org/index.php/AAAI/article/view/5664) algorithm):
- Sort the systems by size (gates amount).
- For each system, run over the observations:
  - For each observation, create all it's uncertain optional observations (by generating all outputs permutations).
  - Calculate the probability of each uncertain observation to occur.
  - For each uncertain observation, run BFS algorithm for diagnosis searching.
  - Calculate the probability of each diagnosis to be true.
- Sum the probabilities of similar diagnosis that came from different observations for the same system.
- Sort the diagnosis by descending probability and return the top 5.

???????????????????????????? The logic can be accessed via the API in `diagnosis_with_uncertain_observations/circuit_parser/api.py`.


## Usage
Create the DB from systems and observations files in `circuits_examples\` directory:
```
  python diagnosis_with_uncertain_observation/manage.py migrate
```
Open django DB shell with:
```
  python diagnosis_with_uncertain_observation/manage.py shell
```
and run the following in it:
```python
  from circuits_parser.api import find_diagnosis_run_time
  find_diagnosis_run_time()
```
Now you have a DB of all the systems, observations (including the uncertain ones) and diagnoses with their probabilities.
- To get the top `n` diagnoses of a system named `system_name` run in django DB shell:
```python
  from circuits_parser.api import top_diagnoses
  best_diagnoses = top_diagnoses(system_name, n)
```

- To save viewable results in `.txt` files run in django DB shell:
```python
  from circuits_parser.api import save_txt_results
  save_txt_results(system_name)
```

- To save pythonic results in `.pickle` files run in django DB shell:
```python
  from circuits_parser.api import save_pickle_results
  save_pickle_results(system_name)
```

All the parameters are configurable in the `config.py` file.


## Assumptions
- The systems are pretty heavy and the algorithm takes not negligible time to run, so we assumed that the probability of more than 3 gates to be faulty is 0.
- The probability of a single observed output to be true is 0.9 ?????????????????????????
- The probability of a single faulty gate is 0.01 ?????????????????????????????????


## Evaluation
