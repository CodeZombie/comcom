from typing import Dict
import pytest
from comcom.playbook.deep_yaml import deep_yaml_load

from rich.console import Console

from comcom.playbook.recipe import Recipe

SIMPLE_RECIPE_YAML: str = """

full_name_template: &full_name_template
    full_name: "{name.honorific} {name.first} {name.last}" 

values:
    <<: *full_name_template
    name:
        honorific: Mr.
        first: Fox
        last: Mulder

recipes:
    head_cannon:
        values:
            <<: *full_name_template
            name:
                honorific: Mrs.
                first: Dana
        recipes: 
            child_a: &child_recipe
                values:
                    <<: *full_name_template
                    name:
                        honorific: Little Mr.
                        first: Luke
                    mom: "{^.full_name}"
                    dad: "{^.^.full_name}"
    reality:
        values:
            <<: *full_name_template
            name:
                honorific: Ms.
                first: Dana
                last: Scully
        recipes:
            child_a:
                <<: *child_recipe
            pet_a:
                <<: *child_recipe
                values:
                    name:
                        honorific: "{^.name.first}'s dog,"
                        first: Queequeg
                
"""

def test_cascading_data_in_recipe():
    recipe_dict = deep_yaml_load(SIMPLE_RECIPE_YAML)
    c = Console()
    c.print(recipe_dict)
    recipe = Recipe.model_validate(recipe_dict)
    recipe.solve()
    assert recipe.values.get('full_name') == "Mr. Fox Mulder"
    head_cannon_recipe = recipe.get_recipe('head_cannon')
    assert head_cannon_recipe.values.get('full_name') == "Mrs. Dana Mulder"
    head_cannon_child_recipe = head_cannon_recipe.get_recipe('child_a')
    assert head_cannon_child_recipe.values.get('full_name') == "Little Mr. Luke Mulder"
    assert head_cannon_child_recipe.values.get('dad') == "Mr. Fox Mulder"
    assert head_cannon_child_recipe.values.get('mom') == "Mrs. Dana Mulder"

    reality_recipe = recipe.get_recipe("reality")
    assert reality_recipe.values.get('full_name') == "Ms. Dana Scully"
    reality_child_recipe = recipe.get_recipe('reality.child_a')
    assert reality_child_recipe.id == "child_a"
    assert reality_child_recipe.values.get('full_name') == "Little Mr. Luke Scully"
    assert reality_child_recipe.values.get('dad') == "Mr. Fox Mulder"
    assert reality_child_recipe.values.get('mom') == "Ms. Dana Scully"

    scullys_dog_recipe = recipe.get_recipe('reality.pet_a')
    assert scullys_dog_recipe.values.get('mom') == "Ms. Dana Scully"
    assert scullys_dog_recipe.values.get('full_name') == "Dana's dog, Queequeg Scully"


def test_flattened_recipe_list():
    recipe = Recipe.model_validate(deep_yaml_load(SIMPLE_RECIPE_YAML))
    flattened_recipe_list: Dict[str, Recipe] = recipe.get_flattened_children()
    assert recipe.id == 'root'
    assert len(flattened_recipe_list.keys()) == 5