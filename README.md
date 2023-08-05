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
- Sort the diagnosis by descending probability.


## Usage
Make sure to [install Django](https://www.w3schools.com/django/django_install_django.php).

Create the DB of systems and observations from the files in `circuits_examples\` directory:
```
  python diagnosis_with_uncertain_observation/manage.py migrate
```
Open django DB shell with
```
  python diagnosis_with_uncertain_observation/manage.py shell
```
and run the following in it:
```python
  from circuits_parser.api import find_diagnosis
  find_diagnosis()
```
Now you have a DB of all the systems, observations (including the uncertain ones) and diagnoses with their probabilities.

- To get the top `n` diagnoses of a system named `system_name` run **in django DB shell**:
```python
  from circuits_parser.api import top_diagnoses
  best_diagnoses = top_diagnoses(system_name, n)
```

- To save viewable results in `.txt` files run **in django DB shell**:
```python
  from circuits_parser.api import save_txt_results
  save_txt_results(system_name)
```

(The API above can be seen in `diagnosis_with_uncertain_observations/circuit_parser/api.py`)


## Assumptions
- The systems are pretty heavy and the algorithm takes not negligible time to run, so we assumed that at most 3 gates can be faulty.
- The probability of a single faulty gate is 0.01
- The optimal probability of a single observed output to be true is 0.99

All the parameters are configurable through the `diagnosis_with_uncertain_observations/circuit_parser/config.py` file.


## Evaluation
We ran the O2D algorithm on the 3 smallest systems:
- c17 (size of 6 gates) - 252 uncertain observations
- 74182 (size of 19 gates) - 111 uncertain observations
- 74283 (size of 36 gates) - 5 uncertain observations

The mean run times of the algorithm on a single observation is dispalyed in the following plot:

![mean run times](/diagnosis_with_uncertain_observation/circuits_parser/results/run_times/mean-run-times-plot.png)

In order to find the optimal probability that represents uncertainty (and to ensure that it really improves the results), at first, we ran the algorithm without considering uncertainty at all. (The results can be seen in `diagnosis_with_uncertain_observations/circuit_parser/results/diagnosis_probabilities/***_1.0.txt` files.)
Our experiments ran over various values of `p=[0.7, 0.75, 0.8, 0.85, 0.9]` and we came to the conclusion that the algorithm performs bad for small `p`s, which means - large uncertainty.
So the next batch of experiments was on `p=[0.91, 0.92, ..., 0.99]`, and we have recognized the same tendency, but here **all of them outperformed** the baseline (where `p=1.0` without uncertainty).

Our results defenetly support the [paper](https://ojs.aaai.org/index.php/AAAI/article/view/5664) conclusion:
> _Experimental evaluation shows that this third algorithm can be very effective in cases where the number of faults is small and the uncertainty over the observations is not large._

(All our experiments results can be seen in `diagnosis_with_uncertain_observations/circuit_parser/results/diagnosis_probabilities/` directory.
