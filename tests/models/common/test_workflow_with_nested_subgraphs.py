import pytest

from comcom.comfy_ui.models.raw.workflow.version_0_4.workflow import Comfy_V0_4_Workflow
from comcom.comfy_ui.models.normalized.workflow.workflow import NormalizedWorkflow
from comcom.comfy_ui.models.normalized.workflow.subgraph_definition import NormalizedSubgraphDefinition
from comcom.comfy_ui.models.raw.node_definitions.version_1_0.node_definitions import Comfy_v1_0_NodeDefinitions

WORKFLOW_WITH_SIMPLE_SUBGRAPH_JSON = """
{
  "id": "02439884-a1c5-449e-bf43-6e05377a45ca",
  "revision": 0,
  "last_node_id": 5,
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
        847.9432373046875,
        391.9666748046875
      ],
      "size": [
        210,
        102
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
        },
        {
          "name": "width",
          "type": "INT",
          "link": null
        },
        {
          "name": "height",
          "type": "INT",
          "link": null
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
          "lastNodeId": 13,
          "lastLinkId": 30,
          "lastRerouteId": 0
        },
        "revision": 0,
        "config": {},
        "name": "New Subgraph",
        "inputNode": {
          "id": -10,
          "bounding": [
            489.2223673566957,
            399.616479457365,
            120,
            120
          ]
        },
        "outputNode": {
          "id": -20,
          "bounding": [
            1542.7275866007196,
            432.33585052546033,
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
              "0": 589.2223510742188,
              "1": 419.6164855957031
            }
          },
          {
            "id": "80ccc863-15ac-407d-b4f8-a1c775f463ad",
            "name": "rotation",
            "type": "COMBO",
            "linkIds": [
              14
            ],
            "pos": {
              "0": 589.2223510742188,
              "1": 439.6164855957031
            }
          },
          {
            "id": "0a225eae-9958-4875-a812-42884a172c56",
            "name": "width",
            "type": "INT",
            "linkIds": [
              26
            ],
            "pos": {
              "0": 589.2223510742188,
              "1": 459.6164855957031
            }
          },
          {
            "id": "7a6cdead-783b-4c2c-a6b0-0c9b920f65c1",
            "name": "height",
            "type": "INT",
            "linkIds": [
              27
            ],
            "pos": {
              "0": 589.2223510742188,
              "1": 479.6164855957031
            }
          }
        ],
        "outputs": [
          {
            "id": "77c545ac-15ba-49d6-936e-ee706be7347b",
            "name": "IMAGE",
            "type": "IMAGE",
            "linkIds": [
              30
            ],
            "localized_name": "IMAGE",
            "pos": {
              "0": 1562.7275390625,
              "1": 452.3358459472656
            }
          }
        ],
        "widgets": [],
        "nodes": [
          {
            "id": 12,
            "type": "0a79d690-2c96-4667-98e4-c0e3d9292a9a",
            "pos": [
              840.2258911132812,
              554.9961547851562
            ],
            "size": [
              210,
              102
            ],
            "flags": {},
            "order": 2,
            "mode": 0,
            "inputs": [
              {
                "localized_name": "width",
                "name": "width",
                "type": "INT",
                "link": 26
              },
              {
                "localized_name": "height",
                "name": "height",
                "type": "INT",
                "link": 27
              }
            ],
            "outputs": [
              {
                "name": "IMAGE",
                "type": "IMAGE",
                "links": [
                  29
                ]
              }
            ],
            "properties": {},
            "widgets_values": [
              512,
              512
            ]
          },
          {
            "id": 2,
            "type": "ImageRotate",
            "pos": [
              804.1942138671875,
              397.6822204589844
            ],
            "size": [
              270,
              58
            ],
            "flags": {},
            "order": 1,
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
                "link": 14
              }
            ],
            "outputs": [
              {
                "localized_name": "IMAGE",
                "name": "IMAGE",
                "type": "IMAGE",
                "links": [
                  15,
                  28
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
            "id": 13,
            "type": "ImageBlend",
            "pos": [
              1174.86474609375,
              473.47052001953125
            ],
            "size": [
              270,
              102
            ],
            "flags": {},
            "order": 0,
            "mode": 0,
            "inputs": [
              {
                "localized_name": "image1",
                "name": "image1",
                "type": "IMAGE",
                "link": 28
              },
              {
                "localized_name": "image2",
                "name": "image2",
                "type": "IMAGE",
                "link": 29
              }
            ],
            "outputs": [
              {
                "localized_name": "IMAGE",
                "name": "IMAGE",
                "type": "IMAGE",
                "links": [
                  30
                ]
              }
            ],
            "properties": {
              "Node name for S&R": "ImageBlend"
            },
            "widgets_values": [
              0.5,
              "normal"
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
            "id": 14,
            "origin_id": -10,
            "origin_slot": 1,
            "target_id": 2,
            "target_slot": 1,
            "type": "COMBO"
          },
          {
            "id": 26,
            "origin_id": -10,
            "origin_slot": 2,
            "target_id": 12,
            "target_slot": 0,
            "type": "INT"
          },
          {
            "id": 27,
            "origin_id": -10,
            "origin_slot": 3,
            "target_id": 12,
            "target_slot": 1,
            "type": "INT"
          },
          {
            "id": 28,
            "origin_id": 2,
            "origin_slot": 0,
            "target_id": 13,
            "target_slot": 0,
            "type": "IMAGE"
          },
          {
            "id": 29,
            "origin_id": 12,
            "origin_slot": 0,
            "target_id": 13,
            "target_slot": 1,
            "type": "IMAGE"
          },
          {
            "id": 30,
            "origin_id": 13,
            "origin_slot": 0,
            "target_id": -20,
            "target_slot": 0,
            "type": "IMAGE"
          }
        ],
        "extra": {}
      },
      {
        "id": "0a79d690-2c96-4667-98e4-c0e3d9292a9a",
        "version": 1,
        "state": {
          "lastGroupId": 0,
          "lastNodeId": 11,
          "lastLinkId": 26,
          "lastRerouteId": 0
        },
        "revision": 0,
        "config": {},
        "name": "New Subgraph",
        "inputNode": {
          "id": -10,
          "bounding": [
            606.59521484375,
            591.4443359375,
            120,
            80
          ]
        },
        "outputNode": {
          "id": -20,
          "bounding": [
            1421.2489013671875,
            611.4443359375,
            120,
            60
          ]
        },
        "inputs": [
          {
            "id": "55f2b76d-158c-44e1-94f6-dc1167b9b4d1",
            "name": "width",
            "type": "INT",
            "linkIds": [
              23
            ],
            "localized_name": "width",
            "pos": {
              "0": 706.59521484375,
              "1": 611.4443359375
            }
          },
          {
            "id": "3b84c5ef-f31e-4d7b-8f88-512fa0004147",
            "name": "height",
            "type": "INT",
            "linkIds": [
              24
            ],
            "localized_name": "height",
            "pos": {
              "0": 706.59521484375,
              "1": 631.4443359375
            }
          }
        ],
        "outputs": [
          {
            "id": "e560d54a-398f-48c8-b9cc-7374e1416ebc",
            "name": "IMAGE",
            "type": "IMAGE",
            "linkIds": [
              26
            ],
            "pos": {
              "0": 1441.2489013671875,
              "1": 631.4443359375
            }
          }
        ],
        "widgets": [],
        "nodes": [
          {
            "id": 10,
            "type": "EmptyImage",
            "pos": [
              786.59521484375,
              582.8987426757812
            ],
            "size": [
              270,
              130
            ],
            "flags": {},
            "order": 0,
            "mode": 0,
            "inputs": [
              {
                "localized_name": "width",
                "name": "width",
                "type": "INT",
                "widget": {
                  "name": "width"
                },
                "link": 23
              },
              {
                "localized_name": "height",
                "name": "height",
                "type": "INT",
                "widget": {
                  "name": "height"
                },
                "link": 24
              }
            ],
            "outputs": [
              {
                "localized_name": "IMAGE",
                "name": "IMAGE",
                "type": "IMAGE",
                "links": [
                  25
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
            "id": 11,
            "type": "ImageBlur",
            "pos": [
              1091.2489013671875,
              579.9899291992188
            ],
            "size": [
              270,
              82
            ],
            "flags": {},
            "order": 1,
            "mode": 0,
            "inputs": [
              {
                "localized_name": "image",
                "name": "image",
                "type": "IMAGE",
                "link": 25
              }
            ],
            "outputs": [
              {
                "localized_name": "IMAGE",
                "name": "IMAGE",
                "type": "IMAGE",
                "links": [
                  26
                ]
              }
            ],
            "properties": {
              "Node name for S&R": "ImageBlur"
            },
            "widgets_values": [
              1,
              1
            ]
          }
        ],
        "groups": [],
        "links": [
          {
            "id": 25,
            "origin_id": 10,
            "origin_slot": 0,
            "target_id": 11,
            "target_slot": 0,
            "type": "IMAGE"
          },
          {
            "id": 23,
            "origin_id": -10,
            "origin_slot": 0,
            "target_id": 10,
            "target_slot": 0,
            "type": "INT"
          },
          {
            "id": 24,
            "origin_id": -10,
            "origin_slot": 1,
            "target_id": 10,
            "target_slot": 1,
            "type": "INT"
          },
          {
            "id": 26,
            "origin_id": 11,
            "origin_slot": 0,
            "target_id": -20,
            "target_slot": 0,
            "type": "IMAGE"
          }
        ],
        "extra": {}
      }
    ]
  },
  "config": {},
  "extra": {
    "ds": {
      "scale": 1.8337760794707332,
      "offset": [
        -379.05721778542363,
        -148.2763711714865
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
    return Comfy_V0_4_Workflow.model_validate_json(WORKFLOW_WITH_SIMPLE_SUBGRAPH_JSON).to_normalized(normalized_node_definitions).to_common(normalized_node_definitions)

def test_workflow_properties(workflow):
    assert workflow.id == "02439884-a1c5-449e-bf43-6e05377a45ca"
    assert len(workflow.nodes) == 6

    image_rotate_node = workflow.get_node_by_id("4:2")
    assert image_rotate_node
    assert image_rotate_node.id == "4:2"
    assert image_rotate_node.get_input_by_name('image')
    assert image_rotate_node.get_input_by_name('image').name == 'image'
    assert image_rotate_node.get_input_by_name('image').is_link == True
    assert image_rotate_node.get_input_by_name('image').value.source_node_id == '1'
    assert image_rotate_node.get_input_by_name('image').value.source_node_output_name == 'IMAGE'

    empty_image_node = workflow.get_node_by_id('4:12:10')
    assert empty_image_node
    assert empty_image_node.id == '4:12:10'
    assert empty_image_node.get_input_by_name('width')
    assert empty_image_node.get_input_by_name('width').name == 'width'
    assert empty_image_node.get_input_by_name('width').is_link == True
    assert empty_image_node.get_input_by_name('width').value.source_node_id == None
    assert empty_image_node.get_input_by_name('width').value.source_node_output_name == None

    preview_image_node = workflow.get_node_by_id('3')
    assert preview_image_node
    assert preview_image_node.id == '3'
    assert preview_image_node.get_input_by_name('images')
    assert preview_image_node.get_input_by_name('images').name == 'images'
    assert preview_image_node.get_input_by_name('images').is_link == True
    assert preview_image_node.get_input_by_name('images').value.source_node_id == '4:13'
    assert preview_image_node.get_input_by_name('images').value.source_node_output_name == 'IMAGE'
