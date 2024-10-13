import json
import urllib.request


class NumericProcessor:
    def __init__(self, computations_list):
        self.computations_list = computations_list
        # You can add more initialization code here if you'd like.

    def run_computations(self):
        pass
        # You will write code here, to go through the self.computations_list.
    
    


def load_computations_list_from_file(filename):
    with open(filename, 'r') as f:
        contents = json.load(f)
        return contents['computations']


def get_mathjs_api_url(expression):
    # Expression is a string such as '1 + 1'.
    # Some characters need to be transformed when they are sent to the api.
    # urllib.parse.quote does this.
    # For example, it turns '+' into the code '%2B' so that the api can receieve it.
    expression = urllib.parse.quote(expression)
    url = 'http://api.mathjs.org/v4/?expr=' + expression
    return url


if __name__ == '__main__':
    computations = load_computations_list_from_file('example.json')
    processor = NumericProcessor(computations)
    processor.run_computations()

