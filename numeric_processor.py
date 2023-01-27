
import json
import urllib.request 
import time
from collections import Counter

class NumericProcessor:
    def __init__(self, filename):
        with open(filename, 'r') as f:
            contents = json.load(f)
            self.computations = contents['computations']
    
    def run_computations(self):
        self.last_result = 0.0
        for computation in self.computations:
            self.last_result = self.run_computation(computation)
    
    def evaluate_ans(self, value):
        if value == 'ANS':
            return self.last_result
        else:
            return value
    
    def evaluate_ans_list(self, values):
        return [self.evaluate_ans(val) for val in values]
    
    def run_computation(self, computation):
        values = self.evaluate_ans_list(computation['values'])
        if computation['operation'] == 'add':
            return self.op_add(values)
        elif computation['operation'] == 'multiply':
            return self.op_multiply(values)
        elif computation['operation'] == 'subtract':
            return self.op_subtract(values)
        elif computation['operation'] == 'divide':
            return self.op_divide(values)
        elif computation['operation'] == 'display':
            return self.op_display(values)
        elif computation['operation'] == 'api-compute':
            return self.op_api_compute(values)
        else:
            raise RuntimeError('unknown operation')
    
    def op_add(self, values):
        return float(values[0]) + float(values[1])
    
    def op_multiply(self, values):
        return float(values[0]) * float(values[1])
        
    def op_subtract(self, values):
        return float(values[0]) - float(values[1])
        
    def op_divide(self, values):
        return float(values[0]) / float(values[1])
        
    def op_display(self, values):
        print(values[0])
        return values[0]
    
    def op_api_compute(self, values):
        expression = values[0]
        expression = expression.replace(' ', '')
        expression = expression.replace('+', '%2b')
        url = 'http://api.mathjs.org/v4/?expr=' + expression
        response = urllib.request.urlopen(url)
        result = response.read().decode('utf-8')
        return float(result)
    
class NumericProcessorBenchmarkCounts(NumericProcessor):
    def __init__(self, filename):
        super().__init__(filename)
        self.benchmark_per_operation = Counter()
    
    def run_computation(self, computation):
        self.benchmark_per_operation[computation['operation']] += 1
        return super().run_computation(computation)
    
    def show_benchmarks(self):
        print(self.benchmark_per_operation)

class NumericProcessorBenchmarkTiming(NumericProcessor):
    def __init__(self, filename):
        super().__init__(filename)
        self.benchmark_per_operation = Counter()
        self.benchmark_duration_per_operation = {}
    
    def run_computation(self, computation):
        self.benchmark_per_operation[computation['operation']] += 1
        started = time.time()
        ret = super().run_computation(computation)
        ended = time.time()
        duration = ended - started
        if computation['operation'] in self.benchmark_duration_per_operation:
            self.benchmark_duration_per_operation[computation['operation']] += duration
        else:
            self.benchmark_duration_per_operation[computation['operation']] = duration
        
        return ret
    
    def show_benchmarks(self):
        for key in self.benchmark_per_operation:
            print(key)
            print('#', self.benchmark_per_operation[key])
            print('avg duration (s)', self.benchmark_duration_per_operation[key] / self.benchmark_per_operation[key])

if __name__ == '__main__':
    o = NumericProcessorBenchmarkTiming('example2.json')
    o.run_computations()
    o.show_benchmarks()

