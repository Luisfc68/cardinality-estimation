from numpy import e, sqrt
import randomhash
from collections.abc import Iterable
from typing import Any
from common import RunResult
from heapq import heappush, heappop

def create_recordinality(k: int):
    MAX_HASH = 2**32 - 1
    hash_family = randomhash.RandomHashFamily(count=1)  # recordinality only uses one hash function
    def recordinality_instance(stream: Iterable[Any]):
        records = set()
        heap = []
        stream_size = 0
        number_of_records = 0
        for element in stream:
            stream_size += 1
            element_hash = hash_family.hash(element) & MAX_HASH
            element_not_in_records = element_hash not in records
            if len(records) < k and element_not_in_records:
                records.add(element_hash)
                heappush(heap, element_hash)
                number_of_records += 1
                continue

            min_record = heap[0]
            if element_not_in_records and element_hash > min_record:
                removed = heappop(heap)
                records.remove(removed)
                records.add(element_hash)
                heappush(heap, element_hash)
                number_of_records += 1
        estimation = (k * (1 + 1/k)**(number_of_records - k + 1)) - 1
        return RunResult(
            {"records": records, "estimation": estimation},
            estimation,
            expected_recordinality_error(stream_size, k)
        )
    return recordinality_instance

def expected_recordinality_error(real_length:int, k: int):
    return sqrt((real_length/(k*e))**(1/k) - 1) # https://inria.hal.science/hal-01197221v1/document