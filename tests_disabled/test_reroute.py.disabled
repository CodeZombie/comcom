import json
import pytest

from comcom.transformers.workflows import Node, NodeDefinition, Link, Workflow

TWO_NODES_WITH_REROUTE_WORKFLOW_JSON = """
{
  "id": "2e482714-1a00-4608-9c2d-4eed8e1e7bf8",
  "revision": 0,
  "last_node_id": 3,
  "last_link_id": 2,
  "nodes": [
    {
      "id": 1,
      "type": "LoadImage",
      "pos": [
        60,
        80
      ],
      "size": [
        274.080078125,
        314
      ],
      "flags": {},
      "order": 0,
      "mode": 0,
      "inputs": [],
      "outputs": [
        {
          "name": "IMAGE",
          "type": "IMAGE",
          "links": [
            1
          ]
        },
        {
          "name": "MASK",
          "type": "MASK",
          "links": null
        }
      ],
      "properties": {
        "Node name for S&R": "LoadImage"
      },
      "widgets_values": [
        "clean.png",
        "image"
      ]
    },
    {
      "id": 3,
      "type": "PreviewImage",
      "pos": [
        550,
        80
      ],
      "size": [
        140,
        26
      ],
      "flags": {},
      "order": 2,
      "mode": 0,
      "inputs": [
        {
          "name": "images",
          "type": "IMAGE",
          "link": 2
        }
      ],
      "outputs": [],
      "properties": {
        "Node name for S&R": "PreviewImage"
      }
    },
    {
      "id": 2,
      "type": "Reroute",
      "pos": [
        410,
        80
      ],
      "size": [
        75,
        26
      ],
      "flags": {},
      "order": 1,
      "mode": 0,
      "inputs": [
        {
          "name": "",
          "type": "*",
          "link": 1
        }
      ],
      "outputs": [
        {
          "name": "",
          "type": "IMAGE",
          "links": [
            2
          ]
        }
      ],
      "properties": {
        "showOutputText": false,
        "horizontal": false
      }
    }
  ],
  "links": [
    [
      1,
      1,
      0,
      2,
      0,
      "*"
    ],
    [
      2,
      2,
      0,
      3,
      0,
      "IMAGE"
    ]
  ],
  "groups": [],
  "config": {},
  "extra": {
    "ds": {
      "scale": 1.2524937364051192,
      "offset": [
        289.62300118049154,
        320.3960528378248
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
def two_nodes_with_reroute_workflow_dict():
    return json.loads(TWO_NODES_WITH_REROUTE_WORKFLOW_JSON)

def test_node_input_extraction(two_nodes_with_reroute_workflow_dict, node_definitions_dict):
    workflow = Workflow.from_workflow_json_dict(two_nodes_with_reroute_workflow_dict, node_definitions_dict)
    
    assert len(workflow.nodes) == 2
    assert isinstance(workflow.get_node_by_id('3').get_input('image').value, Link)
    assert workflow.get_node_by_id('3').get_input('image').value.source_node_id == '1'
    assert workflow.get_node_by_id('3').get_input('image').value.source_output_id == 0
