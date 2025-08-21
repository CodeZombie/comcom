import pytest

from comcom.comfy_ui.models.raw.workflow.version_0_4.workflow import Comfy_V0_4_Workflow
from comcom.comfy_ui.models.normalized.workflow.workflow import NormalizedWorkflow
from comcom.comfy_ui.models.normalized.workflow.subgraph_definition import NormalizedSubgraphDefinition

SUBGRAPH_WORKFLOW_JSON = """
{
  "id": "941084b1-a392-44f4-9064-688e43b2ea48",
  "revision": 0,
  "last_node_id": 8,
  "last_link_id": 12,
  "nodes": [
    {
      "id": 1,
      "type": "LoadImage",
      "pos": [
        70,
        -140
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
            8
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
        "2025-04-14_21-25-34-novaFurryXL_illustriousV6b-565926541.png",
        "image"
      ]
    },
    {
      "id": 2,
      "type": "CheckpointLoaderSimple",
      "pos": [
        70,
        -300
      ],
      "size": [
        270,
        98
      ],
      "flags": {},
      "order": 1,
      "mode": 0,
      "inputs": [],
      "outputs": [
        {
          "name": "MODEL",
          "type": "MODEL",
          "links": [
            10
          ]
        },
        {
          "name": "CLIP",
          "type": "CLIP",
          "links": null
        },
        {
          "name": "VAE",
          "type": "VAE",
          "links": [
            9
          ]
        }
      ],
      "properties": {
        "Node name for S&R": "CheckpointLoaderSimple"
      },
      "widgets_values": [
        "Anything-V3.0-pruned-fp16.safetensors"
      ]
    },
    {
      "id": 6,
      "type": "PreviewImage",
      "pos": [
        980,
        -280
      ],
      "size": [
        140,
        26
      ],
      "flags": {},
      "order": 4,
      "mode": 0,
      "inputs": [
        {
          "name": "images",
          "type": "IMAGE",
          "link": 11
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
      "type": "PrimitiveInt",
      "pos": [
        80,
        230
      ],
      "size": [
        270,
        82
      ],
      "flags": {},
      "order": 2,
      "mode": 0,
      "inputs": [],
      "outputs": [
        {
          "name": "INT",
          "type": "INT",
          "links": [
            12
          ]
        }
      ],
      "properties": {
        "Node name for S&R": "PrimitiveInt"
      },
      "widgets_values": [
        0,
        "randomize"
      ]
    },
    {
      "id": 7,
      "type": "b48931b4-1499-46f5-85c3-1a5ef033a29b",
      "pos": [
        520,
        -300
      ],
      "size": [
        210,
        122
      ],
      "flags": {},
      "order": 3,
      "mode": 0,
      "inputs": [
        {
          "name": "pixels",
          "type": "IMAGE",
          "link": 8
        },
        {
          "name": "vae",
          "type": "VAE",
          "link": 9
        },
        {
          "name": "model",
          "type": "MODEL",
          "link": 10
        },
        {
          "name": "seed",
          "type": "INT",
          "widget": {
            "name": "seed"
          },
          "link": 12
        }
      ],
      "outputs": [
        {
          "name": "IMAGE",
          "type": "IMAGE",
          "links": [
            11
          ]
        }
      ],
      "properties": {},
      "widgets_values": [
        0,
        "euler"
      ]
    }
  ],
  "links": [
    [
      8,
      1,
      0,
      7,
      0,
      "IMAGE"
    ],
    [
      9,
      2,
      2,
      7,
      1,
      "VAE"
    ],
    [
      10,
      2,
      0,
      7,
      2,
      "MODEL"
    ],
    [
      11,
      7,
      0,
      6,
      0,
      "IMAGE"
    ],
    [
      12,
      8,
      0,
      7,
      3,
      "INT"
    ]
  ],
  "groups": [],
  "definitions": {
    "subgraphs": [
      {
        "id": "b48931b4-1499-46f5-85c3-1a5ef033a29b",
        "version": 1,
        "state": {
          "lastGroupId": 0,
          "lastNodeId": 6,
          "lastLinkId": 9,
          "lastRerouteId": 0
        },
        "revision": 0,
        "config": {},
        "name": "New Subgraph",
        "inputNode": {
          "id": -10,
          "bounding": [
            440,
            -204,
            120,
            140
          ]
        },
        "outputNode": {
          "id": -20,
          "bounding": [
            1270,
            -184,
            120,
            60
          ]
        },
        "inputs": [
          {
            "id": "6d48fa68-1a72-42fb-9e5b-26ed31682bbd",
            "name": "pixels",
            "type": "IMAGE",
            "linkIds": [
              4
            ],
            "localized_name": "pixels",
            "pos": {
              "0": 540,
              "1": -184
            }
          },
          {
            "id": "10c6b481-e7be-499c-b4be-7bc274fdde3f",
            "name": "vae",
            "type": "VAE",
            "linkIds": [
              3,
              6
            ],
            "localized_name": "vae",
            "pos": {
              "0": 540,
              "1": -164
            }
          },
          {
            "id": "74435c16-2d81-46f0-bbe6-90eefa31e687",
            "name": "model",
            "type": "MODEL",
            "linkIds": [
              1
            ],
            "localized_name": "model",
            "pos": {
              "0": 540,
              "1": -144
            }
          },
          {
            "id": "cf5c35d1-8a5b-4492-aa25-ab4c893c2dc0",
            "name": "seed",
            "type": "INT",
            "linkIds": [
              8
            ],
            "pos": {
              "0": 540,
              "1": -124
            }
          },
          {
            "id": "7260a55b-a4cf-4b46-a87b-06cc5cfb64dc",
            "name": "sampler_name",
            "type": "COMBO",
            "linkIds": [
              9
            ],
            "label": "model",
            "pos": {
              "0": 540,
              "1": -104
            }
          }
        ],
        "outputs": [
          {
            "id": "640f3519-fa22-41a1-8cbf-2dfa3d6371df",
            "name": "IMAGE",
            "type": "IMAGE",
            "linkIds": [
              7
            ],
            "localized_name": "IMAGE",
            "pos": {
              "0": 1290,
              "1": -164
            }
          }
        ],
        "widgets": [],
        "nodes": [
          {
            "id": 3,
            "type": "KSampler",
            "pos": [
              760,
              -270
            ],
            "size": [
              270,
              262
            ],
            "flags": {},
            "order": 0,
            "mode": 0,
            "inputs": [
              {
                "localized_name": "model",
                "name": "model",
                "type": "MODEL",
                "link": 1
              },
              {
                "localized_name": "positive",
                "name": "positive",
                "type": "CONDITIONING",
                "link": null
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
                "link": 2
              },
              {
                "localized_name": "seed",
                "name": "seed",
                "type": "INT",
                "widget": {
                  "name": "seed"
                },
                "link": 8
              },
              {
                "localized_name": "sampler_name",
                "name": "sampler_name",
                "type": "COMBO",
                "widget": {
                  "name": "sampler_name"
                },
                "link": 9
              }
            ],
            "outputs": [
              {
                "localized_name": "LATENT",
                "name": "LATENT",
                "type": "LATENT",
                "links": [
                  5
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
              "normal",
              1
            ]
          },
          {
            "id": 5,
            "type": "VAEDecode",
            "pos": [
              1070,
              -270
            ],
            "size": [
              140,
              46
            ],
            "flags": {},
            "order": 2,
            "mode": 0,
            "inputs": [
              {
                "localized_name": "samples",
                "name": "samples",
                "type": "LATENT",
                "link": 5
              },
              {
                "localized_name": "vae",
                "name": "vae",
                "type": "VAE",
                "link": 6
              }
            ],
            "outputs": [
              {
                "localized_name": "IMAGE",
                "name": "IMAGE",
                "type": "IMAGE",
                "links": [
                  7
                ]
              }
            ],
            "properties": {
              "Node name for S&R": "VAEDecode"
            }
          },
          {
            "id": 4,
            "type": "VAEEncode",
            "pos": [
              570,
              -430
            ],
            "size": [
              140,
              46
            ],
            "flags": {},
            "order": 1,
            "mode": 0,
            "inputs": [
              {
                "localized_name": "pixels",
                "name": "pixels",
                "type": "IMAGE",
                "link": 4
              },
              {
                "localized_name": "vae",
                "name": "vae",
                "type": "VAE",
                "link": 3
              }
            ],
            "outputs": [
              {
                "localized_name": "LATENT",
                "name": "LATENT",
                "type": "LATENT",
                "links": [
                  2
                ]
              }
            ],
            "properties": {
              "Node name for S&R": "VAEEncode"
            }
          }
        ],
        "groups": [],
        "links": [
          {
            "id": 2,
            "origin_id": 4,
            "origin_slot": 0,
            "target_id": 3,
            "target_slot": 3,
            "type": "LATENT"
          },
          {
            "id": 5,
            "origin_id": 3,
            "origin_slot": 0,
            "target_id": 5,
            "target_slot": 0,
            "type": "LATENT"
          },
          {
            "id": 4,
            "origin_id": -10,
            "origin_slot": 0,
            "target_id": 4,
            "target_slot": 0,
            "type": "IMAGE"
          },
          {
            "id": 3,
            "origin_id": -10,
            "origin_slot": 1,
            "target_id": 4,
            "target_slot": 1,
            "type": "VAE"
          },
          {
            "id": 6,
            "origin_id": -10,
            "origin_slot": 1,
            "target_id": 5,
            "target_slot": 1,
            "type": "VAE"
          },
          {
            "id": 1,
            "origin_id": -10,
            "origin_slot": 2,
            "target_id": 3,
            "target_slot": 0,
            "type": "MODEL"
          },
          {
            "id": 7,
            "origin_id": 5,
            "origin_slot": 0,
            "target_id": -20,
            "target_slot": 0,
            "type": "IMAGE"
          },
          {
            "id": 8,
            "origin_id": -10,
            "origin_slot": 3,
            "target_id": 3,
            "target_slot": 4,
            "type": "INT"
          },
          {
            "id": 9,
            "origin_id": -10,
            "origin_slot": 4,
            "target_id": 3,
            "target_slot": 5,
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
      "scale": 1.279992473170673,
      "offset": [
        390.7111316852628,
        599.2664544931213
      ]
    },
    "frontendVersion": "1.24.0-1"
  },
  "version": 0.4
}
"""

@pytest.fixture
def workflow():
    return Comfy_V0_4_Workflow.model_validate_json(SUBGRAPH_WORKFLOW_JSON)

def test_convert_version_0_4_subgraph_definition_to_normalized(workflow):
    assert len(workflow.subgraph_definitions) == 1
    raw_subgraph_definition = workflow.subgraph_definitions[0]
    normalized_workflow = workflow.to_normalized()
    normalized_subgraph_definition = normalized_workflow.subgraph_definitions[0]

    assert isinstance(normalized_subgraph_definition, NormalizedSubgraphDefinition)
    assert normalized_subgraph_definition.id == raw_subgraph_definition.id
    assert normalized_subgraph_definition.revision == raw_subgraph_definition.revision
    assert normalized_subgraph_definition.version == raw_subgraph_definition.version
    assert len(normalized_subgraph_definition.subgraph_definitions) == len(raw_subgraph_definition.subgraph_definitions)
    assert len(normalized_subgraph_definition.nodes) == len(raw_subgraph_definition.nodes) == 3
    assert len(normalized_subgraph_definition.incoming) == len(raw_subgraph_definition.input_slots) == 5
    assert len(normalized_subgraph_definition.outgoing) == len(raw_subgraph_definition.output_slots) == 1
