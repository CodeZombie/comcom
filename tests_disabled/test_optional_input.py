import json
import pytest

from comcom.transformers.workflows import Node, NodeDefinition, Link

ALL_OPTIONAL_INPUTS_NODE_JSON = """
{
    "id": 1,
    "type": "RegexReplace",
    "pos": [
        640,
        220
    ],
    "size": [
        400,
        292
    ],
    "flags": {},
    "order": 5,
    "mode": 0,
    "inputs": [
        {
            "name": "regex_pattern",
            "type": "STRING",
            "widget": {
                "name": "regex_pattern"
            },
            "link": 1
        },
        {
            "name": "dotall",
            "shape": 7,
            "type": "BOOLEAN",
            "widget": {
                "name": "dotall"
            },
            "link": 5
        }
    ],
    "outputs": [
        {
            "name": "STRING",
            "type": "STRING",
            "links": null
        }
    ],
    "properties": {
        "Node name for S&R": "RegexReplace"
    },
    "widgets_values": [
        "",
        "",
        "",
        true,
        false,
        false,
        0
    ]
}
"""

ONE_OPTIONAL_INPUT_NODE_JSON = """
{
    "id": 3,
    "type": "ControlNetApplyAdvanced",
    "pos": [
        640,
        560
    ],
    "size": [
        270,
        186
    ],
    "flags": {},
    "order": 4,
    "mode": 0,
    "inputs": [
        {
            "name": "positive",
            "type": "CONDITIONING",
            "link": null
        },
        {
            "name": "negative",
            "type": "CONDITIONING",
            "link": 4
        },
        {
            "name": "control_net",
            "type": "CONTROL_NET",
            "link": null
        },
        {
            "name": "image",
            "type": "IMAGE",
            "link": null
        },
        {
            "name": "vae",
            "shape": 7,
            "type": "VAE",
            "link": null
        },
        {
            "name": "start_percent",
            "type": "FLOAT",
            "widget": {
                "name": "start_percent"
            },
            "link": 2
        }
    ],
    "outputs": [
        {
            "name": "positive",
            "type": "CONDITIONING",
            "links": []
        },
        {
            "name": "negative",
            "type": "CONDITIONING",
            "links": null
        }
    ],
    "properties": {
        "Node name for S&R": "ControlNetApplyAdvanced"
    },
    "widgets_values": [
        1,
        0,
        1
    ]
}
"""

@pytest.fixture
def node_definitions_dict():
    d = {}
    with open('tests/data/object_info.json', 'r') as f:
        d = json.load(f)
    return d

@pytest.fixture
def all_optional_node_def():
    return json.loads(ALL_OPTIONAL_INPUTS_NODE_JSON)

@pytest.fixture
def one_optional_node_def():
    return json.loads(ONE_OPTIONAL_INPUT_NODE_JSON)

def test_all_optional_inputs_node_definition(node_definitions_dict):
    node_definitions = NodeDefinition.from_dicts(node_definitions_dict)
    controlnetapplyadvanced_definition = node_definitions['RegexReplace']
    assert controlnetapplyadvanced_definition.id == "RegexReplace"
    assert len(controlnetapplyadvanced_definition.input_names) == 7
    assert len(controlnetapplyadvanced_definition.output_names) == 1

def test_one_optional_input_node_definition(node_definitions_dict):
    node_definitions = NodeDefinition.from_dicts(node_definitions_dict)
    controlnetapplyadvanced_definition = node_definitions['ControlNetApplyAdvanced']
    assert controlnetapplyadvanced_definition.id == "ControlNetApplyAdvanced"
    assert len(controlnetapplyadvanced_definition.input_names) == 8
    assert len(controlnetapplyadvanced_definition.output_names) == 2
    assert 'vae' in controlnetapplyadvanced_definition.input_names

def test_all_optional(all_optional_node_def, node_definitions_dict):
    node = Node.from_node_json_dict(all_optional_node_def, node_definitions_dict)
    assert node.id == 1
    assert node.class_type == 'RegexReplace'
    assert len(node.inputs) == 7
    assert node.get_input('string').value == ''
    assert isinstance(node.get_input('regex_pattern').value, Link)
    assert node.get_input('replace').value == ''
    assert node.get_input('case_insensitive').value == True
    assert node.get_input('multiline').value == False
    assert isinstance(node.get_input('dotall').value, Link)
    assert node.get_input('count').value == 0

def test_one_optional(one_optional_node_def, node_definitions_dict):
    node = Node.from_node_json_dict(one_optional_node_def, node_definitions_dict)
    assert node.id == 3
    assert node.class_type == 'ControlNetApplyAdvanced'
    assert len(node.inputs) == 8

    assert isinstance(node.get_input('positive').value, Link)
    assert node.get_input('positive').value.id == None
    assert node.get_input('negative').value.id == 4
    assert node.get_input('control_net').value.id == None
    assert node.get_input('image').value.id == None
    assert node.get_input('vae').value.id == None
    assert node.get_input('strength').value == 1.0
    assert node.get_input('start_percent').value.id == 2
    assert node.get_input('end_percent').value == 1.0
