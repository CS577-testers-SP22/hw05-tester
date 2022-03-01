from subprocess import Popen, PIPE
from random import random, seed
from tqdm import tqdm
from pprint import pprint
import json
import time

SMALL_TEST_COUNT = 100
MEDIUM_TEST_COUNT = 50
LARGE_TEST_COUNT = 10
SEED = 1234
TEST_FILE = 'tests.json'

seed(SEED)

# 1 to 2000 size
# range from 0 to 2^15

class Timer():
    # context manager to capture stdout
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.t0 = time.time()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print(f'{self.name}: {time.time() - self.t0:.2f}')

def generate_random_input(max_instances=20, max_elements=100, min_value=0, max_value=2**15):
    '''returns a string that is valid input'''
    instances = int(random() * (max_instances)) + 1
    test = f'{instances}'

    for _ in range(instances):
        size = int(random() * (max_elements)) + 1

        test += f'\n{size}'

        test += f'\n{" ".join(str(int(random() * (max_value - min_value)) + min_value) for _ in range(size))}'

    return test + '\n'

def generate_fixed_input(multiplier=1, instances=20, pages=100, cache=10):
    '''returns a string that is valid input'''
    test = f'{instances}'

    for _ in range(instances):
        test += f'\n{cache}'
        test += f'\n{pages}'

        test += f'\n{" ".join(str(int(random() * (multiplier * pages)) + 1) for _ in range(pages))}'

    return test + '\n'

def shell(cmd, stdin=None):
    out, err = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE).communicate(input=stdin.encode())
    return out.decode('utf8'), err.decode('utf8')

get_python = lambda testCase: shell('python3 test.py', stdin=testCase)
get_cpp = lambda testCase: shell('./Inversions', stdin=testCase)

tests = dict()

# manual tests
tests['given-test-0'] = {'input':"2\n5\n5 4 3 2 1\n4\n1 5 9 8\n", 'output':"10\n1\n"}

tests['edge-test-0'] = {'input':"1\n1\n1\n", 'output':"0\n"}
tests['edge-test-1'] = {'input':f"1\n100\n{' '.join('0' for _ in range(100))}\n", 'output':"0\n"}
# tests['edge-test-2'] = {'input':f"1\n1\n200\n{' '.join('0 1' for _ in range(100))}\n", 'output':"200\n"}

# random tests

for i in tqdm(range(SMALL_TEST_COUNT)):
    test = generate_random_input(max_instances=3, max_elements=20, max_value=20)
    python, p_err = get_python(test)
    cpp, c_err1 = get_cpp(test)
    # print(python1)
    if python != cpp or len(python) < 1:
        print(f'Python\n{python}')
        print()
        print(f'Python error\n{p_err}')
        print()
        print(f'C++\n{cpp}')
        print()
        print(f'C++ error\n{c_err1}')
        print()
        print(f'Input\n{test}')
        exit()
    tests[f'small-test-{i}'] = {'input':test, 'output':python}

for i in tqdm(range(MEDIUM_TEST_COUNT)):
    test = generate_random_input(max_instances=20, max_elements=300, max_value=300)
    python, p_err = get_python(test)
    cpp, c_err1 = get_cpp(test)
    # print(python1)
    if python != cpp or len(python) < 1:
        print(f'Python\n{python}')
        print()
        print(f'Python error\n{p_err}')
        print()
        print(f'C++\n{cpp}')
        print()
        print(f'C++ error\n{c_err1}')
        print()
        print(f'Input\n{test}')
        exit()
    tests[f'medium-test-{i}'] = {'input':test, 'output':python}

for i in tqdm(range(LARGE_TEST_COUNT)):
    test = generate_random_input(max_instances=100, max_elements=2000)
    python, p_err = get_python(test)
    cpp, c_err1 = get_cpp(test)
    # print(python1)
    if python != cpp or len(python) < 1:
        print(f'Python\n{python}')
        print()
        print(f'Python error\n{p_err}')
        print()
        print(f'C++\n{cpp}')
        print()
        print(f'C++ error\n{c_err1}')
        print()
        print(f'Input\n{test}')
        exit()
    tests[f'large-test-{i}'] = {'input':test, 'output':python}

# pprint(tests)
with open(TEST_FILE, 'w+') as f:
    json.dump(tests, f, indent=4)
