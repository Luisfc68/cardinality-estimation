from os import path

from common import Estimator, EstimatorResult
from hyper_log_log import create_hyper_log_log
from recordinality import create_recordinality

ITERATIONS = 5
HLL_OBSERVABLES = 4096
RECORDINALITY_K = 4096
VERBOSE = True
DATASET_DIR = "./datasets"
DATASET_NAMES = ["synthetic_1"]

def replicate_experiment(value_stream, estimator_instances: list[Estimator], iterations, verbose=False):
    estimator_results = []
    cont = 0
    estimator_cont = 0
    for estimator in estimator_instances:
        estimator_cont += 1
        results = []
        for _ in range(iterations):
            cont +=1
            results.append(estimator.runner(value_stream))
            if verbose:
                print("Estimator {} iteration {}".format(estimator_cont, cont))
        estimator_results.append(EstimatorResult(estimator.name, results))
        cont = 0
    return estimator_results


if __name__ == '__main__':
    dataset_dir = DATASET_DIR
    dataset_names = DATASET_NAMES
    estimators = [
        Estimator("Hyper Log Log raw", create_hyper_log_log(number_of_observables=HLL_OBSERVABLES, use_correction=False)),
        Estimator("Hyper Log Log with corrections", create_hyper_log_log(number_of_observables=HLL_OBSERVABLES, use_correction=True)),
        Estimator("Recordinality", create_recordinality(k=RECORDINALITY_K)),
    ]
    for dataset_name in dataset_names:
        dataset_path = path.join(dataset_dir, dataset_name)
        with open(str(dataset_path)+".txt", "r") as dataset:
            stream = dataset.read().split()
            experiment_results = replicate_experiment(stream, estimators, ITERATIONS, verbose=VERBOSE)
        with open(str(dataset_path)+".dat", "r") as dataset:
            actual_result = len(dataset.readlines())
        print("Dataset name: {}".format(dataset_name))
        print("Actual result: {}".format(actual_result))
        for experiment_result in experiment_results:
            print("{} result: {} ± {}".format(experiment_result.estimator_name, experiment_result.estimation, actual_result*experiment_result.expected_error))