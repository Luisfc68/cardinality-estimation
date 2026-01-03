import randomhash
from collections.abc import Iterable
from typing import Any
from common import RunResult
from heapq import heappush, heappop
from numpy import sqrt

def expected_kmv_error(k: int):
    return 1/sqrt(k)

def create_k_minimum_values(k: int, max_bits = 32):
    MAX_HASH = 2 ** max_bits - 1
    hash_family = randomhash.RandomHashFamily(count=1)  # recordinality only uses one hash function
    def kmv_instance(stream: Iterable[Any]):
        minimum_records = set()
        # we'll use negative values to be able to work with heapq but to get the max value instead of the min
        heap = []
        for element in stream:
            element_hash = hash_family.hash(element) & MAX_HASH
            element_not_in_records = element_hash not in minimum_records
            if len(minimum_records) < k and element_not_in_records:
                minimum_records.add(element_hash)
                heappush(heap, -element_hash)
                continue

            max_record = -heap[0]
            if element_not_in_records and element_hash < max_record:
                removed = -heappop(heap)
                minimum_records.remove(removed)
                minimum_records.add(element_hash)
                heappush(heap, -element_hash)
        if len(minimum_records) < k:
            estimation = len(minimum_records)
        else:
            max_record = -heap[0]
            estimation = ((k - 1)* 2**max_bits) / max_record
        return RunResult(
            {"minimum_records": minimum_records, "estimation": estimation},
            estimation,
            expected_kmv_error(k)
        )
    return kmv_instance