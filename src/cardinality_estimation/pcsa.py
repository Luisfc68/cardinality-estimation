import randomhash
from collections.abc import Iterable
from typing import Any
from common import RunResult
from numpy import sqrt, log2

def expected_pcsa_error(number_of_observables: int): # extracted from https://algo.inria.fr/flajolet/Publications/src/FlMa85.pdf
    return 0.78 / sqrt(number_of_observables)

def update_bitmap(bitmap: int, value: int, max_bits: int):
    if value == 0:
        return bitmap

    leading_zeros = max_bits - (value & (2**max_bits-1)).bit_length()
    return bitmap | (1 << (max_bits - 1- leading_zeros))

def bitmap_to_r(bitmap: int, max_bits: int):
    count = 0
    mask = 1 << (max_bits - 1)  # MSB
    while count < max_bits and (bitmap & mask) != 0:
        count += 1
        mask >>= 1
    return count

def create_probabilistic_counting_stochastic_average(number_of_observables, hash_length = 32):
    if number_of_observables <= 0 or number_of_observables & (number_of_observables - 1) != 0:
        raise ValueError('Number of observables must be a power of 2')
    CORRECTION_CONSTANT = 0.77351
    prefix_size = int(log2(number_of_observables))
    element_size = hash_length - prefix_size
    mask = (2**hash_length - 1)
    def pcsa_instance(stream: Iterable[Any]):
        hash_family = randomhash.RandomHashFamily(count=1)
        observables = [0] * number_of_observables
        for word in stream:
            word_hash = hash_family.hash(word)
            word_hash = word_hash & mask # to ensure the n bits (32)
            prefix = word_hash >> element_size
            value = word_hash & ((1 << element_size) - 1)
            observables[prefix] = update_bitmap(observables[prefix], value, element_size)

        s_value = 0
        for observable in observables:
            s_value += bitmap_to_r(observable, element_size)
        estimation = (number_of_observables / CORRECTION_CONSTANT) * 2**(s_value/number_of_observables)
        return RunResult(
            { "observables": observables, "estimation": estimation },
            estimation,
            expected_pcsa_error(number_of_observables),
        )
    return pcsa_instance