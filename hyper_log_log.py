import randomhash
from numpy import log2, log, sqrt
from collections.abc import Iterable
from typing import Any
from common import RunResult

def get_pattern_size(map_size: int, value: int):
    if value == 0:
        return map_size + 1
    return map_size - value.bit_length() + 1

def get_correction_constant(number_of_observables: int): # taken from https://algo.inria.fr/flajolet/Publications/FlFuGaMe07.pdf page 14
    if number_of_observables >= 128:
        return 0.7213 / (1 + 1.079/number_of_observables)
    elif number_of_observables >= 64:
        return 0.709
    elif number_of_observables >= 32:
        return 0.697
    else:
        return 0.673

def apply_small_range_correction(observables: list[int], estimation):
    empty_observables = observables.count(0)
    if empty_observables != 0:
        number_of_observables = len(observables)
        return number_of_observables * log(number_of_observables/empty_observables)
    else:
        return estimation


def apply_large_range_correction(estimation, hash_length):
    two_pow_hl = 2**hash_length
    return -two_pow_hl * log(1 - estimation/two_pow_hl)


def create_hyper_log_log(
    number_of_observables = 8,
    hash_length = 32,
    use_correction = True,
):
    if number_of_observables <= 0 or number_of_observables & (number_of_observables - 1) != 0:
        raise ValueError('Number of observables must be a power of 2')
    hash_family = randomhash.RandomHashFamily(count=1) # hll only uses one hash function
    prefix_size = int(log2(number_of_observables))
    element_size = hash_length - prefix_size
    mask = (2**hash_length - 1)
    correction_constant = get_correction_constant(number_of_observables)
    def hll_instance(stream: Iterable[Any], verbose = False):
        observables = [0] * number_of_observables
        for word in stream:
            word_hash = hash_family.hash(word)
            word_hash = word_hash & mask # to ensure the n bits (32)
            prefix = word_hash >> element_size
            value = word_hash & ((1 << element_size) - 1)
            pattern_size = get_pattern_size(element_size, value)
            if verbose:
                print("hash: {:032b}".format(word_hash))
                print("prefix: {:0{}b} -> observable {}".format(prefix, prefix_size, prefix))
                print("value: {:0{}b}".format(value, element_size))
                print("pattern size: ", pattern_size)

            if observables[prefix] < pattern_size:
                observables[prefix] = pattern_size

        z_value = 1/(sum(map(lambda x: 1/2**x, observables)))
        estimation = correction_constant * (number_of_observables ** 2) * z_value
        if not use_correction:
            return RunResult(
                {
                    "observables": observables,
                    "raw_estimation": estimation,
                    "corrected_estimation": None,
                },
                estimation,
                expected_hll_error(number_of_observables),
            )

        if estimation <= 2.5 * number_of_observables:
            corrected_estimation = apply_small_range_correction(observables, estimation)
        elif estimation <= 2**hash_length/30:
            corrected_estimation = estimation
        else:
            corrected_estimation = apply_large_range_correction(estimation, hash_length)
        return RunResult(
        {
                "observables": observables,
                "raw_estimation": estimation,
                "corrected_estimation": corrected_estimation,
            },
            corrected_estimation,
            expected_hll_error(number_of_observables)
        )
    return hll_instance

def expected_hll_error(number_of_observables: int):
    return 1.03896 / sqrt(number_of_observables) # extracted from https://algo.inria.fr/flajolet/Publications/FlFuGaMe07.pdf page 3