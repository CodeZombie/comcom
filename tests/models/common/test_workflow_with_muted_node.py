import pytest

from comcom.comfy_ui.models.raw.workflow.version_0_4.workflow import Comfy_V0_4_Workflow
from comcom.comfy_ui.models.normalized.workflow.workflow import NormalizedWorkflow
from comcom.comfy_ui.models.normalized.workflow.subgraph_definition import NormalizedSubgraphDefinition
from comcom.comfy_ui.models.raw.node_definitions.version_1_0.node_definitions import Comfy_v1_0_NodeDefinitions

WORKFLOW_WITH_MUTED_NODE_JSON = """
{
  "id": "7e553c1e-8d91-49f4-b4ec-e0e49aed6e30",
  "revision": 0,
  "last_node_id": 3,
  "last_link_id": 2,
  "nodes": [
    {
      "id": 1,
      "type": "EmptyImage",
      "pos": [
        422.73236083984375,
        356.6169128417969
      ],
      "size": [
        270,
        130
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
    },
    {
      "id": 3,
      "type": "PreviewImage",
      "pos": [
        1146.1575927734375,
        345.0197448730469
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
      "type": "ImageRotate",
      "pos": [
        799.84130859375,
        357.816650390625
      ],
      "size": [
        270,
        58
      ],
      "flags": {},
      "order": 1,
      "mode": 4,
      "inputs": [
        {
          "name": "image",
          "type": "IMAGE",
          "link": 1
        }
      ],
      "outputs": [
        {
          "name": "IMAGE",
          "type": "IMAGE",
          "links": [
            2
          ]
        }
      ],
      "properties": {
        "Node name for S&R": "ImageRotate"
      },
      "widgets_values": [
        "none"
      ]
    }
  ],
  "links": [
    [
      1,
      1,
      0,
      2,
      0,
      "IMAGE"
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
      "scale": 1.6670691631552117,
      "offset": [
        -126.80376928637611,
        -26.896519731254813
      ]
    },
    "frontendVersion": "1.24.0-1"
  },
  "version": 0.4
}
"""

@pytest.fixture
def workflow():
    normalized_node_definitions = Comfy_v1_0_NodeDefinitions.model_validate_json(open('tests/data/object_info.json').read()).to_normalized()
    return Comfy_V0_4_Workflow.model_validate_json(WORKFLOW_WITH_MUTED_NODE_JSON).to_normalized(normalized_node_definitions).to_common(normalized_node_definitions)

def test_workflow_properties(workflow):
    assert workflow.id == "7e553c1e-8d91-49f4-b4ec-e0e49aed6e30"
    assert len(workflow.nodes) == 2

    preview_image_node = workflow.get_node_by_id('3')
    assert preview_image_node
    assert preview_image_node.id == '3'
    assert preview_image_node.get_input_by_name('images')
    assert preview_image_node.get_input_by_name('images').name == 'images'
    assert preview_image_node.get_input_by_name('images').is_link == True
    assert preview_image_node.get_input_by_name('images').value.source_node_id == '1'
    assert preview_image_node.get_input_by_name('images').value.source_node_output_name == 'IMAGE'
