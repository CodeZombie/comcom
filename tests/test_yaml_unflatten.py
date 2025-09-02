import pytest
from comcom.playbook.deep_yaml.deep_yaml import deep_yaml_load

YAML_TEST_A = """
stats:
    age: 29
    gender: female
    name: Dana
[william]:
    stats:
        age: 3
        gender: male
        name: William
    [clothing, pants]:
        color: blue
    [clothing, hat]:
        size: small
        description:
            fitted: True
[william, clothing, hat]:
    color: red
    description:
        logo: "Nike"
"""

def test_yaml_a():
    dana = deep_yaml_load(YAML_TEST_A)
    assert dana['stats']['age'] == 29
    assert dana['stats']['name'] == "Dana"
    print(dana)
    william = dana['recipes']['william']
    assert william['stats']['age'] == 3
    assert william['stats']['name'] == "William"
    william_clothes = william['recipes']['clothing']

    william_hat = william_clothes['recipes']['hat']
    assert william_hat['color'] == "red"
    assert william_hat['size'] == "small"
    assert william_hat['description']['fitted'] == True
    assert william_hat['description']['logo'] == "Nike"

    william_pants = william_clothes['recipes']['pants']
    assert william_pants['color'] == "blue"