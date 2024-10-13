
import io
import contextlib
import unittest
from unittest.mock import patch, Mock

import numeric_processor

class TestNumericProcessor(unittest.TestCase):
    def test_simple_add(self):
        computations = [
            {"operation": "add", "values": ["1", "2"]},
            {"operation": "display", "values": ["ANS"]}
        ]
        
        result = self.run_and_get_stdout(computations)
        self.assertAlmostEqual(float(result), 3)
    
    
    def test_add(self):
        computations = [
            {"operation": "add", "values": ["1.23", "3.01"]},
            {"operation": "add", "values": ["ANS", "1.01"]},
            {"operation": "display", "values": ["ANS"]}
        ]
        
        result = self.run_and_get_stdout(computations)
        self.assertAlmostEqual(float(result), 5.25)
    
    
    def test_subtract(self):
        computations = [
            {"operation": "add", "values": ["1.23", "3.01"]},
            {"operation": "subtract", "values": ["ANS", "1.01"]},
            {"operation": "display", "values": ["ANS"]}
        ]
        
        result = self.run_and_get_stdout(computations)
        self.assertAlmostEqual(float(result), 3.23)
        
    
    def test_multiply(self):
        computations = [
            {"operation": "add", "values": ["1.23", "3.01"]},
            {"operation": "multiply", "values": ["ANS", "1.1"]},
            {"operation": "display", "values": ["ANS"]}
        ]
        
        result = self.run_and_get_stdout(computations)
        self.assertAlmostEqual(float(result), 4.664)
        
    
    def test_divide(self):
        computations = [
            {"operation": "add", "values": ["1.23", "3.01"]},
            {"operation": "divide", "values": ["ANS", "2.5"]},
            {"operation": "display", "values": ["ANS"]}
        ]
        
        result = self.run_and_get_stdout(computations)
        self.assertAlmostEqual(float(result), 1.696)
    
    
    def test_display(self):
        computations = [
            {"operation": "add", "values": ["3", "4"]},
            {"operation": "display", "values": ["ANS"]},
            {"operation": "add", "values": ["5", "6"]},
            {"operation": "display", "values": ["ANS"]},
            {"operation": "add", "values": ["7", "8"]},
        ]
        
        result = self.run_and_get_stdout(computations)
        result = result.replace('\r\n', '\n').split('\n')
        self.assertEqual(len(result), 2)
        self.assertAlmostEqual(float(result[0]), 7)
        self.assertAlmostEqual(float(result[1]), 11)
    
    
    def test_api_call(self):
        computations = [
            {"operation": "add", "values": ["1.23", "3.01"]},
            {"operation": "api-compute", "values": ["2*3"]},
            {"operation": "display", "values": ["ANS"]}
        ]
        
        result = self.run_with_mocked_api_result(computations, b'6.0',
            'http://api.mathjs.org/v4/?expr=2%2A3')
        self.assertAlmostEqual(float(result), 6)
        
    
    def test_api_call_with_plus_and_parens(self):
        computations = [
            {"operation": "add", "values": ["1.23", "3.01"]},
            {"operation": "api-compute", "values": ["2*(3+5)"]},
            {"operation": "display", "values": ["ANS"]}
        ]
        
        result = self.run_with_mocked_api_result(computations, b'16.0',
            'http://api.mathjs.org/v4/?expr=2%2A%283%2B5%29')
        self.assertAlmostEqual(float(result), 16)
    
    
    def test_benchmark_counts(self):
        computations = [
            {"operation": "add", "values": ["1.23", "3.01"]},
            {"operation": "add", "values": ["ANS", "1.01"]},
            {"operation": "subtract", "values": ["ANS", "1.01"]},
            {"operation": "display", "values": ["ANS"]}
        ]
        
        result = self.run_and_get_stats(computations, 
            numeric_processor.OperationCounterNumericProcessor)
        
        result.sort()
        self.assertEqual(len(result), 4)
        self.assertAlmostEqual(float(result[0]), 4.24)
        self.assertEqual(result[1], 'operation: add, count: 2')
        self.assertEqual(result[2], 'operation: display, count: 1')
        self.assertEqual(result[3], 'operation: subtract, count: 1')
    
    def run_and_get_stdout(self, computations):
        instance = numeric_processor.NumericProcessor(computations)
        capture_stdout = io.StringIO()
        with contextlib.redirect_stdout(capture_stdout):
            instance.run_computations()
            
        result = capture_stdout.getvalue()
        return result.strip()
        
    def run_and_get_stats(self, computations, cls):
        instance = cls(computations)
        capture_stdout = io.StringIO()
        with contextlib.redirect_stdout(capture_stdout):
            instance.run_computations()
            instance.show_statistics()
            
        result = capture_stdout.getvalue()
        return result.strip().replace('\r\n', '\n').split('\n')
    
    def run_with_mocked_api_result(self, computations, mock_api_result_in_bytes,
            assert_called_with):

        actually_hit_api = False
        if actually_hit_api:
            return self.run_and_get_stdout(computations)
        else:
            @patch('numeric_processor.urllib.request.urlopen')
            def run_with_mock(mock_urlopen):
                m = Mock()
                m.read.side_effect = [mock_api_result_in_bytes]
                mock_urlopen.return_value = m
                ret = self.run_and_get_stdout(computations)
                mock_urlopen.assert_called_with(assert_called_with)
                return ret
                
            return run_with_mock()

if __name__ == "__main__":
    unittest.main()
