import json
import pytest

from comcom.transformers.workflows import Workflow, Link


TWO_NODES_WORKFLOW_JSON = """
{
  "id": "bb53cfff-fb44-4427-a715-5a58e1dcfb18",
  "revision": 0,
  "last_node_id": 4,
  "last_link_id": 4,
  "nodes": [
    {
      "id": 3,
      "type": "GetImageSize",
      "pos": [
        600,
        360
      ],
      "size": [
        140,
        66
      ],
      "flags": {},
      "order": 0,
      "mode": 0,
      "inputs": [
        {
          "name": "image",
          "type": "IMAGE",
          "link": null
        }
      ],
      "outputs": [
        {
          "name": "width",
          "type": "INT",
          "links": [
            2
          ]
        },
        {
          "name": "height",
          "type": "INT",
          "links": [
            3
          ]
        },
        {
          "name": "batch_size",
          "type": "INT",
          "links": [
            4
          ]
        }
      ],
      "properties": {
        "Node name for S&R": "GetImageSize"
      }
    },
    {
      "id": 4,
      "type": "EmptyImage",
      "pos": [
        840,
        340
      ],
      "size": [
        270,
        130
      ],
      "flags": {},
      "order": 1,
      "mode": 0,
      "inputs": [
        {
          "name": "width",
          "type": "INT",
          "widget": {
            "name": "width"
          },
          "link": 2
        },
        {
          "name": "height",
          "type": "INT",
          "widget": {
            "name": "height"
          },
          "link": 3
        },
        {
          "name": "batch_size",
          "type": "INT",
          "widget": {
            "name": "batch_size"
          },
          "link": 4
        }
      ],
      "outputs": [
        {
          "name": "IMAGE",
          "type": "IMAGE",
          "links": null
        }
      ],
      "properties": {
        "Node name for S&R": "EmptyImage"
      },
      "widgets_values": [
        512,
        512,
        1,
        0
      ]
    }
  ],
  "links": [
    [
      2,
      3,
      0,
      4,
      0,
      "INT"
    ],
    [
      3,
      3,
      1,
      4,
      1,
      "INT"
    ],
    [
      4,
      3,
      2,
      4,
      2,
      "INT"
    ]
  ],
  "groups": [],
  "config": {},
  "extra": {
    "ds": {
      "scale": 1.1386306694591972,
      "offset": [
        112.58258822101928,
        193.5232846477942
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
def two_nodes_workflow():
    return json.loads(TWO_NODES_WORKFLOW_JSON)


def test_node_a(two_nodes_workflow, node_definitions_dict):
    workflow = Workflow.from_workflow_json_dict(two_nodes_workflow, node_definitions_dict)
    node_a = workflow.get_node_by_id('3')
    node_b = workflow.get_node_by_id('4')
    assert node_a.id == 3
    assert node_a.class_type == "GetImageSize"
    assert len(node_a.inputs) == 1
    assert len(node_a.outputs) == 3

    
    assert node_b.id == 4
    assert node_b.class_type == "EmptyImage"
    assert len(node_b.inputs) == 4
    assert len(node_b.outputs) == 1

def test_node_connections(two_nodes_workflow, node_definitions_dict):
    workflow = Workflow.from_workflow_json_dict(two_nodes_workflow, node_definitions_dict)
    node_b = workflow.get_node_by_id('4')

    assert isinstance(node_b.inputs[0].value, Link)
    assert node_b.inputs[0].value.source_node_id == '3'
    assert node_b.inputs[0].value.source_output_id == 0

    assert isinstance(node_b.inputs[1].value, Link)
    assert node_b.inputs[1].value.source_node_id == '3'
    assert node_b.inputs[1].value.source_output_id == 1

    assert isinstance(node_b.inputs[2].value, Link)
    assert node_b.inputs[2].value.source_node_id == '3'
    assert node_b.inputs[2].value.source_output_id == 2