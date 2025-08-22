import pytest

from comcom.comfy_ui.models.raw.workflow.version_0_4.workflow import Comfy_V0_4_Workflow
from comcom.comfy_ui.models.normalized.workflow.workflow import NormalizedWorkflow
from comcom.comfy_ui.models.normalized.workflow.subgraph_definition import NormalizedSubgraphDefinition
from comcom.comfy_ui.models.raw.node_definitions.version_1_0.node_definitions import Comfy_v1_0_NodeDefinitions

WORKFLOW_WITH_MUTED_NODES_AND_REROUTES_JSON = """
{
  "id": "7e553c1e-8d91-49f4-b4ec-e0e49aed6e30",
  "revision": 0,
  "last_node_id": 12,
  "last_link_id": 15,
  "nodes": [
    {
      "id": 5,
      "type": "Reroute",
      "pos": [
        1162.5535888671875,
        428.5994873046875
      ],
      "size": [
        75,
        26
      ],
      "flags": {},
      "order": 6,
      "mode": 0,
      "inputs": [
        {
          "name": "",
          "type": "*",
          "link": 5
        }
      ],
      "outputs": [
        {
          "name": "",
          "type": "IMAGE",
          "links": [
            6
          ]
        }
      ],
      "properties": {
        "showOutputText": false,
        "horizontal": false
      }
    },
    {
      "id": 6,
      "type": "Reroute",
      "pos": [
        823.0357055664062,
        566.166259765625
      ],
      "size": [
        75,
        26
      ],
      "flags": {},
      "order": 4,
      "mode": 0,
      "inputs": [
        {
          "name": "",
          "type": "*",
          "link": 7
        }
      ],
      "outputs": [
        {
          "name": "",
          "type": "IMAGE",
          "links": [
            8
          ]
        }
      ],
      "properties": {
        "showOutputText": false,
        "horizontal": false
      }
    },
    {
      "id": 4,
      "type": "Reroute",
      "pos": [
        620.6845092773438,
        480.5869445800781
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
          "link": 3
        }
      ],
      "outputs": [
        {
          "name": "",
          "type": "IMAGE",
          "links": [
            4,
            7
          ]
        }
      ],
      "properties": {
        "showOutputText": false,
        "horizontal": false
      }
    },
    {
      "id": 1,
      "type": "EmptyImage",
      "pos": [
        217.58184814453125,
        355.017333984375
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
            3,
            10
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
      "order": 3,
      "mode": 4,
      "inputs": [
        {
          "name": "image",
          "type": "IMAGE",
          "link": 4
        }
      ],
      "outputs": [
        {
          "name": "IMAGE",
          "type": "IMAGE",
          "links": [
            5
          ]
        }
      ],
      "properties": {
        "Node name for S&R": "ImageRotate"
      },
      "widgets_values": [
        "none"
      ]
    },
    {
      "id": 3,
      "type": "PreviewImage",
      "pos": [
        1385.29931640625,
        415.80267333984375
      ],
      "size": [
        140,
        26
      ],
      "flags": {},
      "order": 9,
      "mode": 0,
      "inputs": [
        {
          "name": "images",
          "type": "IMAGE",
          "link": 6
        }
      ],
      "outputs": [],
      "properties": {
        "Node name for S&R": "PreviewImage"
      },
      "widgets_values": []
    },
    {
      "id": 8,
      "type": "Reroute",
      "pos": [
        1045.7818603515625,
        567.3658447265625
      ],
      "size": [
        75,
        26
      ],
      "flags": {},
      "order": 7,
      "mode": 0,
      "inputs": [
        {
          "name": "",
          "type": "*",
          "link": 8
        }
      ],
      "outputs": [
        {
          "name": "",
          "type": "IMAGE",
          "links": [
            9
          ]
        }
      ],
      "properties": {
        "showOutputText": false,
        "horizontal": false
      }
    },
    {
      "id": 7,
      "type": "PreviewImage",
      "pos": [
        1386.8992919921875,
        560.567626953125
      ],
      "size": [
        140,
        26
      ],
      "flags": {},
      "order": 10,
      "mode": 0,
      "inputs": [
        {
          "name": "images",
          "type": "IMAGE",
          "link": 9
        }
      ],
      "outputs": [],
      "properties": {
        "Node name for S&R": "PreviewImage"
      }
    },
    {
      "id": 10,
      "type": "PreviewImage",
      "pos": [
        1385.6998291015625,
        665.3424682617188
      ],
      "size": [
        140,
        26
      ],
      "flags": {},
      "order": 11,
      "mode": 0,
      "inputs": [
        {
          "name": "images",
          "type": "IMAGE",
          "link": 15
        }
      ],
      "outputs": [],
      "properties": {
        "Node name for S&R": "PreviewImage"
      }
    },
    {
      "id": 11,
      "type": "Reroute",
      "pos": [
        811.03857421875,
        668.5415649414062
      ],
      "size": [
        75,
        26
      ],
      "flags": {},
      "order": 5,
      "mode": 0,
      "inputs": [
        {
          "name": "",
          "type": "*",
          "link": 12
        }
      ],
      "outputs": [
        {
          "name": "",
          "type": "IMAGE",
          "links": [
            14
          ]
        }
      ],
      "properties": {
        "showOutputText": false,
        "horizontal": false
      }
    },
    {
      "id": 12,
      "type": "ImageRotate",
      "pos": [
        1052.580322265625,
        677.7391357421875
      ],
      "size": [
        270,
        58
      ],
      "flags": {},
      "order": 8,
      "mode": 4,
      "inputs": [
        {
          "name": "image",
          "type": "IMAGE",
          "link": 14
        }
      ],
      "outputs": [
        {
          "name": "IMAGE",
          "type": "IMAGE",
          "links": [
            15
          ]
        }
      ],
      "properties": {
        "Node name for S&R": "ImageRotate"
      },
      "widgets_values": [
        "none"
      ]
    },
    {
      "id": 9,
      "type": "Reroute",
      "pos": [
        620.2846069335938,
        664.54248046875
      ],
      "size": [
        75,
        26
      ],
      "flags": {},
      "order": 2,
      "mode": 0,
      "inputs": [
        {
          "name": "",
          "type": "*",
          "link": 10
        }
      ],
      "outputs": [
        {
          "name": "",
          "type": "IMAGE",
          "links": [
            12
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
      3,
      1,
      0,
      4,
      0,
      "*"
    ],
    [
      4,
      4,
      0,
      2,
      0,
      "IMAGE"
    ],
    [
      5,
      2,
      0,
      5,
      0,
      "*"
    ],
    [
      6,
      5,
      0,
      3,
      0,
      "IMAGE"
    ],
    [
      7,
      4,
      0,
      6,
      0,
      "*"
    ],
    [
      8,
      6,
      0,
      8,
      0,
      "*"
    ],
    [
      9,
      8,
      0,
      7,
      0,
      "IMAGE"
    ],
    [
      10,
      1,
      0,
      9,
      0,
      "*"
    ],
    [
      12,
      9,
      0,
      11,
      0,
      "*"
    ],
    [
      14,
      11,
      0,
      12,
      0,
      "IMAGE"
    ],
    [
      15,
      12,
      0,
      10,
      0,
      "IMAGE"
    ]
  ],
  "groups": [],
  "config": {},
  "extra": {
    "ds": {
      "scale": 1.3777431100456294,
      "offset": [
        -40.28471228448237,
        -50.7207784300051
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
    return Comfy_V0_4_Workflow.model_validate_json(WORKFLOW_WITH_MUTED_NODES_AND_REROUTES_JSON).to_normalized(normalized_node_definitions).to_common(normalized_node_definitions)

def test_workflow_properties(workflow):
    assert workflow.id == "7e553c1e-8d91-49f4-b4ec-e0e49aed6e30"
    assert len(workflow.nodes) == 4

    preview_image_a = workflow.get_node_by_id('3')
    assert preview_image_a
    assert preview_image_a.id == '3'
    assert preview_image_a.get_input_by_name('images')
    assert preview_image_a.get_input_by_name('images').name == 'images'
    assert preview_image_a.get_input_by_name('images').is_link == True
    assert preview_image_a.get_input_by_name('images').value.source_node_id == '1'
    assert preview_image_a.get_input_by_name('images').value.source_node_output_name == 'IMAGE'

    preview_image_b = workflow.get_node_by_id('7')
    assert preview_image_b
    assert preview_image_b.id == '7'
    assert preview_image_b.get_input_by_name('images')
    assert preview_image_b.get_input_by_name('images').name == 'images'
    assert preview_image_b.get_input_by_name('images').is_link == True
    assert preview_image_b.get_input_by_name('images').value.source_node_id == '1'
    assert preview_image_b.get_input_by_name('images').value.source_node_output_name == 'IMAGE'

    preview_image_c = workflow.get_node_by_id('10')
    assert preview_image_c
    assert preview_image_c.id == '10'
    assert preview_image_c.get_input_by_name('images')
    assert preview_image_c.get_input_by_name('images').name == 'images'
    assert preview_image_c.get_input_by_name('images').is_link == True
    assert preview_image_c.get_input_by_name('images').value.source_node_id == '1'
    assert preview_image_c.get_input_by_name('images').value.source_node_output_name == 'IMAGE'