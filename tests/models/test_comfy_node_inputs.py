import pytest

from typing import List, Dict

from comcom.comfy_ui.definition.node_definitions import NodeDefinitions
from comcom.comfy_ui.workflow_graph.workflow import ComfyWorkflow
from comcom.comfy_ui.workflow_graph.input import ComfyInput

TWO_NODES_WORKFLOW_JSON = """
{
  "id": "349c8114-196b-4aec-88c7-3542a6f0f801",
  "revision": 0,
  "last_node_id": 7,
  "last_link_id": 6,
  "nodes": [
    {
      "id": 3,
      "type": "PrimitiveInt",
      "pos": [
        560,
        -100
      ],
      "size": [
        270,
        82
      ],
      "flags": {},
      "order": 0,
      "mode": 0,
      "inputs": [],
      "outputs": [
        {
          "name": "INT",
          "type": "INT",
          "links": [
            2
          ]
        }
      ],
      "properties": {
        "Node name for S&R": "PrimitiveInt"
      },
      "widgets_values": [
        1337,
        "decrement"
      ]
    },
    {
      "id": 5,
      "type": "PrimitiveFloat",
      "pos": [
        560,
        40
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
            3
          ]
        }
      ],
      "properties": {
        "Node name for S&R": "PrimitiveFloat"
      },
      "widgets_values": [
        0.5
      ]
    },
    {
      "id": 2,
      "type": "KSampler",
      "pos": [
        970,
        -280
      ],
      "size": [
        270,
        262
      ],
      "flags": {},
      "order": 3,
      "mode": 0,
      "inputs": [
        {
          "name": "model",
          "type": "MODEL",
          "link": 1
        },
        {
          "name": "positive",
          "type": "CONDITIONING",
          "link": null
        },
        {
          "name": "negative",
          "type": "CONDITIONING",
          "link": null
        },
        {
          "name": "latent_image",
          "type": "LATENT",
          "link": null
        },
        {
          "name": "steps",
          "type": "INT",
          "widget": {
            "name": "steps"
          },
          "link": 2
        },
        {
          "name": "denoise",
          "type": "FLOAT",
          "widget": {
            "name": "denoise"
          },
          "link": 3
        }
      ],
      "outputs": [
        {
          "name": "LATENT",
          "type": "LATENT",
          "links": [
            4
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
      "id": 1,
      "type": "CheckpointLoaderSimple",
      "pos": [
        560,
        -280
      ],
      "size": [
        270,
        98
      ],
      "flags": {},
      "order": 2,
      "mode": 0,
      "inputs": [],
      "outputs": [
        {
          "name": "MODEL",
          "type": "MODEL",
          "links": [
            1
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
            5
          ]
        }
      ],
      "properties": {
        "Node name for S&R": "CheckpointLoaderSimple"
      },
      "widgets_values": [
        "model.safetensors"
      ]
    },
    {
      "id": 6,
      "type": "VAEDecode",
      "pos": [
        1350,
        -260
      ],
      "size": [
        140,
        46
      ],
      "flags": {},
      "order": 4,
      "mode": 0,
      "inputs": [
        {
          "name": "samples",
          "type": "LATENT",
          "link": 4
        },
        {
          "name": "vae",
          "type": "VAE",
          "link": 5
        }
      ],
      "outputs": [
        {
          "name": "IMAGE",
          "type": "IMAGE",
          "links": [
            6
          ]
        }
      ],
      "properties": {
        "Node name for S&R": "VAEDecode"
      }
    },
    {
      "id": 7,
      "type": "PreviewImage",
      "pos": [
        1550,
        -260
      ],
      "size": [
        140,
        26
      ],
      "flags": {},
      "order": 5,
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
      "MODEL"
    ],
    [
      2,
      3,
      0,
      2,
      4,
      "INT"
    ],
    [
      3,
      5,
      0,
      2,
      5,
      "FLOAT"
    ],
    [
      4,
      2,
      0,
      6,
      0,
      "LATENT"
    ],
    [
      5,
      1,
      2,
      6,
      1,
      "VAE"
    ],
    [
      6,
      6,
      0,
      7,
      0,
      "IMAGE"
    ]
  ],
  "groups": [],
  "config": {},
  "extra": {
    "ds": {
      "scale": 1.6670691631552157,
      "offset": [
        -356.569703277405,
        461.99160764610036
      ]
    },
    "frontendVersion": "1.24.0-1"
  },
  "version": 0.4
}
"""

@pytest.fixture
def node_definitions():
    return NodeDefinitions.model_validate_json(open('tests/data/object_info.json').read())

@pytest.fixture
def workflow():
    return ComfyWorkflow.model_validate_json(TWO_NODES_WORKFLOW_JSON)

def test_node_definition(workflow: ComfyWorkflow, node_definitions: NodeDefinitions):
    ksampler_node = workflow.get_node('2')
    ksampler_node_def = node_definitions.get_node_definition(ksampler_node.type)

    ksampler_node_inputs: Dict[str, ComfyInput] = ksampler_node.get_inputs(node_definitions.get_node_definition(ksampler_node.type))
    assert len(ksampler_node_inputs.values()) == 11

    model_input = ksampler_node.get_input('model', ksampler_node_def)    
    model_input.name == "model"
    model_input.name == "MODEL"
    model_input.value == '1'
    model_input.is_link == True

    positive_input = ksampler_node.get_input('positive', ksampler_node_def)    
    positive_input.name == "positive"
    positive_input.name == "CONDITIONING"
    positive_input.value == None
    positive_input.is_link == True

    seed_input = ksampler_node.get_input('seed', ksampler_node_def)    
    seed_input.name == "seed"
    seed_input.name == "INT"
    seed_input.value == '0'
    seed_input.is_link == False

    steps_input = ksampler_node.get_input('steps', ksampler_node_def)    
    steps_input.name == "steps"
    steps_input.name == "INT"
    steps_input.value == '2'
    steps_input.is_link == True

    cfg_input = ksampler_node.get_input('cfg', ksampler_node_def)    
    cfg_input.name == "cfg"
    cfg_input.name == "FLOAT"
    cfg_input.value == '8.0'
    cfg_input.is_link == False

    denoise_input = ksampler_node.get_input('denoise', ksampler_node_def)    
    denoise_input.name == "denoise"
    denoise_input.name == "FLOAT"
    denoise_input.value == '3'
    denoise_input.is_link == False
