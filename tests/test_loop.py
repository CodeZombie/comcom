import json
import pytest

from comcom.transformers.workflows import Workflow, Link

JSON_DATA = """
{
  "id": "bb53cfff-fb44-4427-a715-5a58e1dcfb18",
  "revision": 0,
  "last_node_id": 9,
  "last_link_id": 8,
  "nodes": [
    {
      "id": 6,
      "type": "PrimitiveFloat",
      "pos": [
        190,
        350
      ],
      "size": [
        270,
        58
      ],
      "flags": {},
      "order": 0,
      "mode": 0,
      "inputs": [],
      "outputs": [
        {
          "name": "FLOAT",
          "type": "FLOAT",
          "links": [
            5
          ]
        }
      ],
      "properties": {
        "Node name for S&R": "PrimitiveFloat"
      },
      "widgets_values": [
        0
      ]
    },
    {
      "id": 7,
      "type": "PrimitiveFloat",
      "pos": [
        200,
        490
      ],
      "size": [
        270,
        58
      ],
      "flags": {},
      "order": 1,
      "mode": 0,
      "inputs": [],
      "outputs": [
        {
          "name": "FLOAT",
          "type": "FLOAT",
          "links": [
            6
          ]
        }
      ],
      "properties": {
        "Node name for S&R": "PrimitiveFloat"
      },
      "widgets_values": [
        0
      ]
    },
    {
      "id": 5,
      "type": "ControlNetApplyAdvanced",
      "pos": [
        610,
        350
      ],
      "size": [
        270,
        186
      ],
      "flags": {},
      "order": 2,
      "mode": 0,
      "inputs": [
        {
          "name": "positive",
          "type": "CONDITIONING",
          "link": 8
        },
        {
          "name": "negative",
          "type": "CONDITIONING",
          "link": null
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
          "name": "strength",
          "type": "FLOAT",
          "widget": {
            "name": "strength"
          },
          "link": 5
        },
        {
          "name": "end_percent",
          "type": "FLOAT",
          "widget": {
            "name": "end_percent"
          },
          "link": 6
        }
      ],
      "outputs": [
        {
          "name": "positive",
          "type": "CONDITIONING",
          "links": [
            7
          ]
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
    },
    {
      "id": 8,
      "type": "ConditioningConcat",
      "pos": [
        630,
        200
      ],
      "size": [
        228.38671875,
        46
      ],
      "flags": {},
      "order": 3,
      "mode": 0,
      "inputs": [
        {
          "name": "conditioning_to",
          "type": "CONDITIONING",
          "link": null
        },
        {
          "name": "conditioning_from",
          "type": "CONDITIONING",
          "link": 7
        }
      ],
      "outputs": [
        {
          "name": "CONDITIONING",
          "type": "CONDITIONING",
          "links": [
            8
          ]
        }
      ],
      "properties": {
        "Node name for S&R": "ConditioningConcat"
      }
    }
  ],
  "links": [
    [
      5,
      6,
      0,
      5,
      5,
      "FLOAT"
    ],
    [
      6,
      7,
      0,
      5,
      6,
      "FLOAT"
    ],
    [
      7,
      5,
      0,
      8,
      1,
      "CONDITIONING"
    ],
    [
      8,
      8,
      0,
      5,
      0,
      "CONDITIONING"
    ]
  ],
  "groups": [],
  "config": {},
  "extra": {
    "ds": {
      "scale": 1.6670691631552113,
      "offset": [
        -31.876170107654154,
        -8.819624021249085
      ]
    },
    "frontendVersion": "1.24.0-1"
  },
  "version": 0.4
}
"""


@pytest.fixture
def node_definitions_dict():
    d = {}
    with open('tests/data/object_info.json', 'r') as f:
        d = json.load(f)
    return d

@pytest.fixture
def loop_workflow():
    return json.loads(JSON_DATA)

def test_apply_controlnet_node(loop_workflow, node_definitions_dict):
    workflow = Workflow.from_workflow_json_dict(loop_workflow, node_definitions_dict)
    apply_controlnet_node = workflow.get_node_by_id('5')

    assert apply_controlnet_node.get_input('positive').value.id == 8
    assert apply_controlnet_node.get_input('negative').value.id == None
    assert apply_controlnet_node.get_input('control_net').value.id == None
    assert apply_controlnet_node.get_input('image').value.id == None
    assert apply_controlnet_node.get_input('vae').value.id == None
    assert apply_controlnet_node.get_input('strength').value.source_node_id == '6'
    assert apply_controlnet_node.get_input('strength').value.source_output_id == 0
    assert apply_controlnet_node.get_input('start_percent').value == 0
    assert apply_controlnet_node.get_input('end_percent').value.source_node_id == '7'
    assert apply_controlnet_node.get_input('end_percent').value.source_output_id == 0

def test_conditioning_node(loop_workflow, node_definitions_dict):
    workflow = Workflow.from_workflow_json_dict(loop_workflow, node_definitions_dict)
    conditioning_concat_node = workflow.get_node_by_id('8')

    assert conditioning_concat_node.get_input('conditioning_to').value.id == None
    assert conditioning_concat_node.get_input('conditioning_from').value.id == 7
    assert conditioning_concat_node.get_input('conditioning_from').value.source_node_id == '5'
    assert conditioning_concat_node.get_input('conditioning_from').value.source_output_id == 0