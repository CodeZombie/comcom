import pytest

from comcom.comfy_ui.models.raw.workflow.version_0_4.workflow import Comfy_V0_4_Workflow
from comcom.comfy_ui.models.normalized.workflow.workflow import NormalizedWorkflow
from comcom.comfy_ui.models.normalized.workflow.subgraph_definition import NormalizedSubgraphDefinition
from comcom.comfy_ui.models.raw.node_definitions.version_1_0.node_definitions import Comfy_v1_0_NodeDefinitions

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
def node_definitions():
    return Comfy_v1_0_NodeDefinitions.model_validate_json(open('tests/data/object_info.json').read()).to_normalized()

@pytest.fixture
def workflow(node_definitions):
    return Comfy_V0_4_Workflow.model_validate_json(TWO_NODES_WORKFLOW_JSON).to_normalized(node_definitions)

def test_workflow_properties(workflow):
    assert workflow.id == "bb53cfff-fb44-4427-a715-5a58e1dcfb18"
    assert workflow.revision == 0
    assert len(workflow.get_node('3').inputs) == 1
    assert len(workflow.get_node('3').outputs) == 3

def test_nodes(workflow):
    assert len(workflow.nodes) == 2

def test_convert_version_0_4_workflow_to_normalized(workflow):
    assert isinstance(workflow, NormalizedWorkflow)
    assert workflow.id == workflow.id
    assert workflow.revision == workflow.revision
    assert workflow.version == workflow.version
    assert len(workflow.subgraph_definitions) == len(workflow.subgraph_definitions)
    assert len(workflow.nodes) == 2
