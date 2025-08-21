import json
import pytest

from comcom.transformers.workflows import Node, NodeDefinition, Link

ONE_NODE_JSON = """
{
    "id": 4,
    "type": "KSampler",
    "pos": [
        218.38662719726562,
        285.707763671875
    ],
    "size": [
        270,
        262
    ],
    "flags": {},
    "order": 1,
    "mode": 0,
    "inputs": [
        {
        "localized_name": "model",
        "name": "model",
        "type": "MODEL",
        "link": 9
        },
        {
        "localized_name": "positive",
        "name": "positive",
        "type": "CONDITIONING",
        "link": 11
        },
        {
        "localized_name": "negative",
        "name": "negative",
        "type": "CONDITIONING",
        "link": null
        },
        {
        "localized_name": "latent_image",
        "name": "latent_image",
        "type": "LATENT",
        "link": 14
        },
        {
        "localized_name": "steps",
        "name": "steps",
        "type": "INT",
        "widget": {
            "name": "steps"
        },
        "link": 13
        }
    ],
    "outputs": [
        {
        "localized_name": "LATENT",
        "name": "LATENT",
        "type": "LATENT",
        "links": [
            6,
            8
        ]
        }
    ],
    "properties": {
        "Node name for S&R": "KSampler"
    },
    "widgets_values": [
        0,
        "randomize",
        20,
        8,
        "euler",
        "simple",
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
def one_node():
    node_dict = json.loads(ONE_NODE_JSON)
    return node_dict


def test_node_definition(node_definitions_dict):
    node_definitions = NodeDefinition.from_dicts(node_definitions_dict)
    ksampler_definition = node_definitions['KSampler']
    assert len(ksampler_definition.input_names) == 11
    assert ksampler_definition.id == "KSampler"
    assert len(ksampler_definition.output_names) == 1

def test_node_input_extraction(one_node, node_definitions_dict):
    node_defs = NodeDefinition.from_dicts(node_definitions_dict)
    input_map = node_defs[one_node.get('type')].get_input_map_from_node_definition_dict(one_node)

    assert isinstance(input_map["model"], Link)
    assert input_map["model"].id == 9

    assert input_map["seed"] == 0

    assert isinstance(input_map["steps"], Link)
    assert input_map["steps"].id == 13

    assert input_map["cfg"] == 8

    assert input_map["sampler_name"] == "euler"

    assert input_map["scheduler"] == "simple"

    assert isinstance(input_map["positive"], Link)
    assert input_map["positive"].id == 11

    assert isinstance(input_map["negative"], Link)
    assert input_map["negative"].id == None

    assert isinstance(input_map["latent_image"], Link)
    assert input_map["latent_image"].id == 14

    assert input_map["denoise"] == 1
    

def test_node_basics(one_node, node_definitions_dict):
    node = Node.from_node_json_dict(one_node, node_definitions_dict)
    assert node.id == 4
    assert node.class_type == "KSampler"
    assert len(node.inputs) == 11

def test_node_widget_values(one_node, node_definitions_dict):
    node = Node.from_node_json_dict(one_node, node_definitions_dict)
    assert node.get_input('seed').value == 0
    assert node.get_input('cfg').value == 8.0
    assert node.get_input('sampler_name').value == "euler"
    assert node.get_input('scheduler').value == "simple"
    assert node.get_input('denoise').value == 1.0