import pytest

from typing import List, Dict

from comcom.comfy_ui.models.raw.workflow.version_0_4.node import Comfy_V0_4_Node
from comcom.comfy_ui.models.raw.workflow.version_0_4.workflow import Comfy_V0_4_Workflow
from comcom.comfy_ui.models.raw.workflow.version_0_4.link_input import Comfy_V0_4_LinkInput

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
        "diffusion_model.safetensors"
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
def workflow():
    return Comfy_V0_4_Workflow.model_validate_json(TWO_NODES_WORKFLOW_JSON)

def test_node_definition(workflow: Comfy_V0_4_Workflow):
    assert len(workflow.nodes) == 6

    ksampler_node = workflow.get_node('2')
    assert len(ksampler_node.link_inputs) == 6
    assert ksampler_node.get_link_input('model').name == 'model'
    assert ksampler_node.get_link_input('model').type == 'MODEL'
    assert ksampler_node.get_link_input('model').link == '1'

    assert ksampler_node.get_link_input('steps').name == 'steps'
    assert ksampler_node.get_link_input('steps').type == 'INT'
    assert ksampler_node.get_link_input('steps').link == '2'
    assert ksampler_node.get_link_input('steps').widget_name == 'steps'

    assert ksampler_node.get_link_input('negative').name == 'negative'
    assert ksampler_node.get_link_input('negative').type == 'CONDITIONING'
    assert ksampler_node.get_link_input('negative').link is None

    assert ksampler_node.get_link_input('latent_image').name == 'latent_image'
    assert ksampler_node.get_link_input('latent_image').type == 'LATENT'
    assert ksampler_node.get_link_input('latent_image').link == None


    assert ksampler_node.outputs[0].name == 'LATENT'
    assert ksampler_node.outputs[0].type == 'LATENT'
    assert ksampler_node.outputs[0].links == ['4']


    vae_decode_node = workflow.get_node('6')
    assert len(vae_decode_node.link_inputs) == 2

    assert vae_decode_node.get_link_input('samples').name == 'samples'
    assert vae_decode_node.get_link_input('samples').type == 'LATENT'
    assert vae_decode_node.get_link_input('samples').link == '4'

    assert vae_decode_node.get_link_input('vae').name == 'vae'
    assert vae_decode_node.get_link_input('vae').type == 'VAE'
    assert vae_decode_node.get_link_input('vae').link == '5'