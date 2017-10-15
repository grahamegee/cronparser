import os
import pytest
import yaml
from cronparser.parse import parse

dir_path = os.path.dirname(os.path.realpath(__file__))

with open(f'{dir_path}/parser_tests.yaml') as f:
    test_data = yaml.load(f) 

@pytest.mark.parametrize('input,expected',[
   (test['input'], test['expected']) for test in test_data
])
def test_parser(input, expected):
    assert parse(input) == expected
