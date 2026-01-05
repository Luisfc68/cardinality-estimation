from numpy import average, std

class RunResult:
    def __init__(self, raw_data, result, expected_error):
        self.raw_data = raw_data
        self.result = result
        self.expected_error = expected_error

class Estimator:
    def __init__(self, name, runner):
        self.runner = runner
        self.name = name

class EstimatorResult:
    def __init__(self, estimator_name, results: list[RunResult]):
        self.results = results
        self.estimator_name = estimator_name
        self.estimation = average(list(map(lambda x: x.result, results)))
        self.standard_error = std(list(map(lambda x: x.result, results)))
        # the expected error depends on the observables and the stream size in some cases,
        # so it doesn't vary per execution, we can either take the first or make the average,
        # the number will be the same
        self.expected_error = results[0].expected_error