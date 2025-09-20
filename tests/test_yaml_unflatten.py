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

YAML_TEST_B = """
inventories:
    inventory_a: &inventory_a
        values:
            inventory: "badge"
templates:
    outfit_a: &outfit_a
        values:
            outfit_name: "fbi_costume"

            
[costume]:
    <<: *outfit_a
    <<: *inventory_a
"""

def test_deep_yaml():
    fbi_guy = deep_yaml_load(YAML_TEST_B)
    print(fbi_guy)
    assert fbi_guy['recipes']['costume']
    assert fbi_guy['recipes']['costume']['values']
    assert fbi_guy['recipes']['costume']['values']['outfit_name'] == "fbi_costume"
    assert fbi_guy['recipes']['costume']['values']['inventory'] == "badge"
