from numpy import average

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
        self.expected_error = average(list(map(lambda x: x.expected_error, results)))