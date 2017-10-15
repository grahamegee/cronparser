import os
import pytest
import yaml
from cronparser.parse import parse

dir_path = os.path.dirname(os.path.realpath(__file__))

with open(f'{dir_path}/parser_tests.yaml') as f:
    test_data = yaml.load(f) 

@pytest.mark.parametrize('cronline,expected',[
   (test['cronline'], test['expected']) for test in test_data if not test.get('error')
])
def test_parser_valid_cases(cronline, expected):
    actual = parse(cronline)
    assert parse(cronline) == expected

@pytest.mark.parametrize('cronline,expected',[
   (test['cronline'], test['expected']) for test in test_data if test.get('error')
])
def test_parser_syntax_errors(cronline, expected):
    with pytest.raises(SyntaxError) as excinfo:
        parse(cronline)
    assert str(excinfo.value) == expected['value']
