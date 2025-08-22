import pytest

from comcom.comfy_ui.models.raw.workflow.version_0_4.workflow import Comfy_V0_4_Workflow
from comcom.comfy_ui.models.normalized.workflow.workflow import NormalizedWorkflow
from comcom.comfy_ui.models.normalized.workflow.subgraph_definition import NormalizedSubgraphDefinition
from comcom.comfy_ui.models.raw.node_definitions.version_1_0.node_definitions import Comfy_v1_0_NodeDefinitions

WORKFLOW_WITH_SUBGRAPH_WIDGETS_JSON = """
{
  "id": "02439884-a1c5-449e-bf43-6e05377a45ca",
  "revision": 0,
  "last_node_id": 4,
  "last_link_id": 4,
  "nodes": [
    {
      "id": 1,
      "type": "LoadImage",
      "pos": [
        367.3896789550781,
        405.6490783691406
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
            3
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
        "ComfyUI_00033_.png",
        "image"
      ]
    },
    {
      "id": 3,
      "type": "PreviewImage",
      "pos": [
        1269.428466796875,
        423.43408203125
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
          "link": 4
        }
      ],
      "outputs": [],
      "properties": {
        "Node name for S&R": "PreviewImage"
      },
      "widgets_values": []
    },
    {
      "id": 4,
      "type": "958f4d94-38a9-4ed2-9e09-2de399857e0c",
      "pos": [
        867.40087890625,
        415.3589782714844
      ],
      "size": [
        210,
        58
      ],
      "flags": {
        "collapsed": false
      },
      "order": 1,
      "mode": 0,
      "inputs": [
        {
          "name": "image",
          "type": "IMAGE",
          "link": 3
        }
      ],
      "outputs": [
        {
          "name": "IMAGE",
          "type": "IMAGE",
          "links": [
            4
          ]
        }
      ],
      "properties": {},
      "widgets_values": [
        "none"
      ]
    }
  ],
  "links": [
    [
      3,
      1,
      0,
      4,
      0,
      "IMAGE"
    ],
    [
      4,
      4,
      0,
      3,
      0,
      "IMAGE"
    ]
  ],
  "groups": [],
  "definitions": {
    "subgraphs": [
      {
        "id": "958f4d94-38a9-4ed2-9e09-2de399857e0c",
        "version": 1,
        "state": {
          "lastGroupId": 0,
          "lastNodeId": 3,
          "lastLinkId": 3,
          "lastRerouteId": 0
        },
        "revision": 0,
        "config": {},
        "name": "New Subgraph",
        "inputNode": {
          "id": -10,
          "bounding": [
            690.6282958984375,
            441.42457580566406,
            120,
            80
          ]
        },
        "outputNode": {
          "id": -20,
          "bounding": [
            1200.6282958984375,
            441.42457580566406,
            120,
            60
          ]
        },
        "inputs": [
          {
            "id": "27aaa1f9-e12a-405e-bb6b-c49543d3b82b",
            "name": "image",
            "type": "IMAGE",
            "linkIds": [
              1
            ],
            "localized_name": "image",
            "pos": {
              "0": 790.6282958984375,
              "1": 461.424560546875
            }
          },
          {
            "id": "3184dcba-d8f9-479f-8f56-f271f1aba328",
            "name": "rotation",
            "type": "COMBO",
            "linkIds": [
              3
            ],
            "pos": {
              "0": 790.6282958984375,
              "1": 481.424560546875
            }
          }
        ],
        "outputs": [
          {
            "id": "77c545ac-15ba-49d6-936e-ee706be7347b",
            "name": "IMAGE",
            "type": "IMAGE",
            "linkIds": [
              2
            ],
            "localized_name": "IMAGE",
            "pos": {
              "0": 1220.6282958984375,
              "1": 461.424560546875
            }
          }
        ],
        "widgets": [],
        "nodes": [
          {
            "id": 2,
            "type": "ImageRotate",
            "pos": [
              885.628662109375,
              456.9407043457031
            ],
            "size": [
              270,
              58
            ],
            "flags": {},
            "order": 0,
            "mode": 0,
            "inputs": [
              {
                "localized_name": "image",
                "name": "image",
                "type": "IMAGE",
                "link": 1
              },
              {
                "localized_name": "rotation",
                "name": "rotation",
                "type": "COMBO",
                "widget": {
                  "name": "rotation"
                },
                "link": 3
              }
            ],
            "outputs": [
              {
                "localized_name": "IMAGE",
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
        "groups": [],
        "links": [
          {
            "id": 1,
            "origin_id": -10,
            "origin_slot": 0,
            "target_id": 2,
            "target_slot": 0,
            "type": "IMAGE"
          },
          {
            "id": 2,
            "origin_id": 2,
            "origin_slot": 0,
            "target_id": -20,
            "target_slot": 0,
            "type": "IMAGE"
          },
          {
            "id": 3,
            "origin_id": -10,
            "origin_slot": 1,
            "target_id": 2,
            "target_slot": 1,
            "type": "COMBO"
          }
        ],
        "extra": {}
      }
    ]
  },
  "config": {},
  "extra": {
    "ds": {
      "scale": 1.3777431100456294,
      "offset": [
        -36.99844805912934,
        -39.39031805804839
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
    return Comfy_V0_4_Workflow.model_validate_json(WORKFLOW_WITH_SUBGRAPH_WIDGETS_JSON).to_normalized(normalized_node_definitions).to_common(normalized_node_definitions)

def test_workflow_properties(workflow):
    assert workflow.id == "02439884-a1c5-449e-bf43-6e05377a45ca"
    assert len(workflow.nodes) == 3

    image_rotate_node = workflow.get_node_by_id("4:2")
    assert image_rotate_node
    assert image_rotate_node.id == "4:2"
    assert image_rotate_node.get_input_by_name('image')
    assert image_rotate_node.get_input_by_name('image').name == 'image'
    assert image_rotate_node.get_input_by_name('image').is_link == True
    assert image_rotate_node.get_input_by_name('image').value.source_node_id == '1'
    assert image_rotate_node.get_input_by_name('image').value.source_node_output_name == 'IMAGE'

    assert image_rotate_node.get_input_by_name('rotation')
    assert image_rotate_node.get_input_by_name('rotation').name == 'rotation'
    assert image_rotate_node.get_input_by_name('rotation').is_link == False
    assert image_rotate_node.get_input_by_name('rotation').value == 'none'
    

    preview_image = workflow.get_node_by_id('3')
    assert preview_image
    assert preview_image.id == '3'
    assert preview_image.get_input_by_name('images')
    assert preview_image.get_input_by_name('images').name == 'images'
    assert preview_image.get_input_by_name('images').is_link == True
    assert preview_image.get_input_by_name('images').value.source_node_id == '4:2'
    assert preview_image.get_input_by_name('images').value.source_node_output_name == 'IMAGE'
