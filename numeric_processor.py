
import json
import urllib.request 
import time

def computations_list_from_file(filename):
    with open(filename, 'r') as f:
        contents = json.load(f)
        return contents['computations']

class NumericProcessor:
    def __init__(self, computations_list):
        self.last_result = None
        self.computations = computations_list
    
    def run_computations(self):
        for computation in self.computations:
            self.last_result = self.run_computation(computation)
    
    def replace_ans_with_last_result(self, values):
        new_values = []
        for value in values:
            if value == 'ANS':
                new_values.append(self.last_result)
            else:
                new_values.append(value)
        
        return new_values
    
    def run_computation(self, computation):
        values = self.replace_ans_with_last_result(computation['values'])
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
    
    def prepareQuery(self, expression):
        expression = urllib.parse.quote(expression)
        url = 'http://api.mathjs.org/v4/?expr=' + expression
        return url
    
    def op_api_compute(self, values):
        expression = values[0]
        url = self.prepareQuery(expression)
        response = urllib.request.urlopen(url)
        result = response.read().decode('utf-8')
        return float(result)
    
    
    
class NumericProcessorBenchmarkCounts(NumericProcessor):
    def __init__(self, filename):
        super().__init__(filename)
        self.benchmark_per_operation = {}
    
    def run_computation(self, computation):
        op = computation['operation']
        if op in self.benchmark_per_operation:
            self.benchmark_per_operation[op] += 1
        else:
            self.benchmark_per_operation[op] = 1
        
        return super().run_computation(computation)
    
    def show_benchmarks(self):
        print(self.benchmark_per_operation)

class NumericProcessorBenchmarkTiming(NumericProcessor):
    def __init__(self, filename):
        super().__init__(filename)
        self.benchmark_per_operation = {}
        self.benchmark_duration_per_operation = {}
    
    def run_computation(self, computation):
        started = time.time()
        ret = super().run_computation(computation)
        ended = time.time()
        duration = ended - started
        
        op = computation['operation']
        if op in self.benchmark_per_operation:
            self.benchmark_per_operation[op] += 1
        else:
            self.benchmark_per_operation[op] = 1
            
        if op in self.benchmark_duration_per_operation:
            self.benchmark_duration_per_operation[op] += duration
        else:
            self.benchmark_duration_per_operation[op] = duration
        
        return ret
    
    def show_benchmarks(self):
        for key in self.benchmark_per_operation:
            print(key)
            print('#', self.benchmark_per_operation[key])
            print('avg duration (s)', self.benchmark_duration_per_operation[key] / self.benchmark_per_operation[key])

if __name__ == '__main__':
    computations = computations_list_from_file('example2.json')
    o = NumericProcessorBenchmarkTiming(computations)
    o.run_computations()
    o.show_benchmarks()

