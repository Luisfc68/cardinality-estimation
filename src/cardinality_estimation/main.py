from os import path
from common import Estimator, EstimatorResult
from hyper_log_log import create_hyper_log_log
from kmv import create_k_minimum_values
from pcsa import create_probabilistic_counting_stochastic_average
from recordinality import create_recordinality
import csv

ITERATIONS = 100
HLL_OBSERVABLES = 4096
KMV_K = 4096
RECORDINALITY_K = 2048
PCSA_OBSERVABLES = 128 # importante comentar que n >> m sino no estima bien
VERBOSE = False
DATASET_DIR = "./datasets"
DATASET_NAMES = ["dracula", "crusoe", "iliad", "synthetic_1", "quijote", "test"]
RESULT_FILENAME = "estimations"

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

def normalize_str(value: str):
    return value.lower().replace(" ", "_")

if __name__ == '__main__':
    dataset_dir = DATASET_DIR
    dataset_names = DATASET_NAMES
    estimators = [
        #Estimator("Hyper Log Log raw", create_hyper_log_log(number_of_observables=HLL_OBSERVABLES, use_correction=False)),
        #Estimator("Hyper Log Log with corrections 1", create_hyper_log_log(number_of_observables=HLL_OBSERVABLES, use_correction=True)),
        #Estimator("Hyper Log Log with corrections 2", create_hyper_log_log(number_of_observables=HLL_OBSERVABLES**2, use_correction=True)),
        #Estimator("Hyper Log Log with corrections 3", create_hyper_log_log(number_of_observables=HLL_OBSERVABLES**4, use_correction=True)),
        #Estimator("Hyper Log Log with corrections 4", create_hyper_log_log(number_of_observables=HLL_OBSERVABLES**6, use_correction=True)),
        #Estimator("Hyper Log Log with corrections 5", create_hyper_log_log(number_of_observables=HLL_OBSERVABLES**8, use_correction=True)),
        #Estimator("Recordinality 1", create_recordinality(k=RECORDINALITY_K)),
        #Estimator("Recordinality 2", create_recordinality(k=RECORDINALITY_K**2)),
        #Estimator("Recordinality 3", create_recordinality(k=RECORDINALITY_K**4)),
        #Estimator("Recordinality 4", create_recordinality(k=RECORDINALITY_K**6)),
        Estimator("Recordinality 5", create_recordinality(k=RECORDINALITY_K**8)),
        #Estimator("PCSA 1", create_probabilistic_counting_stochastic_average(number_of_observables=PCSA_OBSERVABLES)),
        #Estimator("PCSA 2", create_probabilistic_counting_stochastic_average(number_of_observables=PCSA_OBSERVABLES**2)),
        #Estimator("PCSA 3", create_probabilistic_counting_stochastic_average(number_of_observables=PCSA_OBSERVABLES**4)),
        #Estimator("PCSA 4", create_probabilistic_counting_stochastic_average(number_of_observables=PCSA_OBSERVABLES**6)),
        #Estimator("PCSA 5", create_probabilistic_counting_stochastic_average(number_of_observables=PCSA_OBSERVABLES**8)),
        #Estimator("KMV 1", create_k_minimum_values(k=KMV_K)),
        #Estimator("KMV 2", create_k_minimum_values(k=KMV_K**2)),
        #Estimator("KMV 3", create_k_minimum_values(k=KMV_K**4)),
        #Estimator("KMV 4", create_k_minimum_values(k=KMV_K**6)),
        #Estimator("KMV 5", create_k_minimum_values(k=KMV_K**8)),
    ]
    results = []
    for dataset_name in dataset_names:
        dataset_path = path.join(dataset_dir, dataset_name)
        with open(str(dataset_path)+".txt", "r") as dataset:
            stream = dataset.read().split()
            experiment_results = replicate_experiment(stream, estimators, ITERATIONS, verbose=VERBOSE)
        with open(str(dataset_path)+".dat", "r") as dataset:
            actual_result = len(dataset.readlines())
        print("Dataset name: {}".format(dataset_name))
        print("Actual result: {}".format(actual_result))
        result = {
            "dataset": dataset_name,
            "actual_value": actual_result,
            "stream_size": len(stream)
        }
        for experiment_result in experiment_results:
            print("{} result: {} ± {}".format(experiment_result.estimator_name, experiment_result.estimation, actual_result*experiment_result.expected_error))
            result[normalize_str(experiment_result.estimator_name) + "_estimation"] = experiment_result.estimation
            result[normalize_str(experiment_result.estimator_name) + "_theoretical_relative_error"] = experiment_result.expected_error
            result[normalize_str(experiment_result.estimator_name) + "_theoretical_error"] = actual_result*experiment_result.expected_error
            result[normalize_str(experiment_result.estimator_name) + "_standard_error"] = experiment_result.standard_error
            result[normalize_str(experiment_result.estimator_name) + "_relative_error"] = 100 * abs(experiment_result.standard_error / actual_result - experiment_result.expected_error) / experiment_result.expected_error
        results.append(result)
    with open(RESULT_FILENAME+".csv", "w", newline="") as csvfile:
        fieldnames = ['dataset', 'actual_value', "stream_size"]
        for estimator in estimators:
            fieldnames.append(normalize_str(estimator.name) + "_estimation")
            fieldnames.append(normalize_str(estimator.name) + "_theoretical_relative_error")
            fieldnames.append(normalize_str(estimator.name) + "_theoretical_error")
            fieldnames.append(normalize_str(estimator.name) + "_standard_error")
            fieldnames.append(normalize_str(estimator.name) + "_relative_error")
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)