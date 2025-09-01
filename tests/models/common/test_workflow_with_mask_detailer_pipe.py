import pytest

from typing import List, Dict

from comcom.comfy_ui.models.raw.node_definitions.version_1_0.node_definitions import Comfy_v1_0_NodeDefinitions
from comcom.comfy_ui.models.raw.workflow.version_0_4.workflow import Comfy_V0_4_Workflow
from comcom.comfy_ui.models.common.workflow import Workflow


NODE_DEFINITIONS_JSON = """
{
    "MaskDetailerPipe": {
        "input": {
            "required": {
                "image": [
                    "IMAGE"
                ],
                "mask": [
                    "MASK"
                ],
                "basic_pipe": [
                    "BASIC_PIPE"
                ],
                "guide_size": [
                    "FLOAT",
                    {
                        "default": 512,
                        "min": 64,
                        "max": 16384,
                        "step": 8
                    }
                ],
                "guide_size_for": [
                    "BOOLEAN",
                    {
                        "default": true,
                        "label_on": "mask bbox",
                        "label_off": "crop region"
                    }
                ],
                "max_size": [
                    "FLOAT",
                    {
                        "default": 1024,
                        "min": 64,
                        "max": 16384,
                        "step": 8
                    }
                ],
                "mask_mode": [
                    "BOOLEAN",
                    {
                        "default": true,
                        "label_on": "masked only",
                        "label_off": "whole"
                    }
                ],
                "seed": [
                    "INT",
                    {
                        "default": 0,
                        "min": 0,
                        "max": 18446744073709551615
                    }
                ],
                "steps": [
                    "INT",
                    {
                        "default": 20,
                        "min": 1,
                        "max": 10000
                    }
                ],
                "cfg": [
                    "FLOAT",
                    {
                        "default": 8.0,
                        "min": 0.0,
                        "max": 100.0
                    }
                ],
                "sampler_name": [
                    [
                        "euler",
                        "euler_cfg_pp",
                        "euler_ancestral",
                        "euler_ancestral_cfg_pp",
                        "heun",
                        "heunpp2",
                        "dpm_2",
                        "dpm_2_ancestral",
                        "lms",
                        "dpm_fast",
                        "dpm_adaptive",
                        "dpmpp_2s_ancestral",
                        "dpmpp_2s_ancestral_cfg_pp",
                        "dpmpp_sde",
                        "dpmpp_sde_gpu",
                        "dpmpp_2m",
                        "dpmpp_2m_cfg_pp",
                        "dpmpp_2m_sde",
                        "dpmpp_2m_sde_gpu",
                        "dpmpp_3m_sde",
                        "dpmpp_3m_sde_gpu",
                        "ddpm",
                        "lcm",
                        "ipndm",
                        "ipndm_v",
                        "deis",
                        "res_multistep",
                        "res_multistep_cfg_pp",
                        "res_multistep_ancestral",
                        "res_multistep_ancestral_cfg_pp",
                        "gradient_estimation",
                        "gradient_estimation_cfg_pp",
                        "er_sde",
                        "seeds_2",
                        "seeds_3",
                        "ddim",
                        "uni_pc",
                        "uni_pc_bh2"
                    ]
                ],
                "scheduler": [
                    [
                        "normal",
                        "karras",
                        "exponential",
                        "sgm_uniform",
                        "simple",
                        "ddim_uniform",
                        "beta",
                        "linear_quadratic",
                        "kl_optimal",
                        "AYS SDXL",
                        "AYS SD1",
                        "AYS SVD",
                        "GITS[coeff=1.2]",
                        "LTXV[default]",
                        "OSS FLUX",
                        "OSS Wan"
                    ]
                ],
                "denoise": [
                    "FLOAT",
                    {
                        "default": 0.5,
                        "min": 0.0001,
                        "max": 1.0,
                        "step": 0.01
                    }
                ],
                "feather": [
                    "INT",
                    {
                        "default": 5,
                        "min": 0,
                        "max": 100,
                        "step": 1
                    }
                ],
                "crop_factor": [
                    "FLOAT",
                    {
                        "default": 3.0,
                        "min": 1.0,
                        "max": 10,
                        "step": 0.1
                    }
                ],
                "drop_size": [
                    "INT",
                    {
                        "min": 1,
                        "max": 16384,
                        "step": 1,
                        "default": 10
                    }
                ],
                "refiner_ratio": [
                    "FLOAT",
                    {
                        "default": 0.2,
                        "min": 0.0,
                        "max": 1.0
                    }
                ],
                "batch_size": [
                    "INT",
                    {
                        "default": 1,
                        "min": 1,
                        "max": 100
                    }
                ],
                "cycle": [
                    "INT",
                    {
                        "default": 1,
                        "min": 1,
                        "max": 10,
                        "step": 1
                    }
                ]
            },
            "optional": {
                "refiner_basic_pipe_opt": [
                    "BASIC_PIPE"
                ],
                "detailer_hook": [
                    "DETAILER_HOOK"
                ],
                "inpaint_model": [
                    "BOOLEAN",
                    {
                        "default": false,
                        "label_on": "enabled",
                        "label_off": "disabled"
                    }
                ],
                "noise_mask_feather": [
                    "INT",
                    {
                        "default": 20,
                        "min": 0,
                        "max": 100,
                        "step": 1
                    }
                ],
                "bbox_fill": [
                    "BOOLEAN",
                    {
                        "default": false,
                        "label_on": "enabled",
                        "label_off": "disabled"
                    }
                ],
                "contour_fill": [
                    "BOOLEAN",
                    {
                        "default": true,
                        "label_on": "enabled",
                        "label_off": "disabled"
                    }
                ],
                "scheduler_func_opt": [
                    "SCHEDULER_FUNC"
                ]
            }
        },
        "input_order": {
            "required": [
                "image",
                "mask",
                "basic_pipe",
                "guide_size",
                "guide_size_for",
                "max_size",
                "mask_mode",
                "seed",
                "steps",
                "cfg",
                "sampler_name",
                "scheduler",
                "denoise",
                "feather",
                "crop_factor",
                "drop_size",
                "refiner_ratio",
                "batch_size",
                "cycle"
            ],
            "optional": [
                "refiner_basic_pipe_opt",
                "detailer_hook",
                "inpaint_model",
                "noise_mask_feather",
                "bbox_fill",
                "contour_fill",
                "scheduler_func_opt"
            ]
        },
        "output": [
            "IMAGE",
            "IMAGE",
            "IMAGE",
            "BASIC_PIPE",
            "BASIC_PIPE"
        ],
        "output_is_list": [
            false,
            true,
            true,
            false,
            false
        ],
        "output_name": [
            "image",
            "cropped_refined",
            "cropped_enhanced_alpha",
            "basic_pipe",
            "refiner_basic_pipe_opt"
        ],
        "name": "MaskDetailerPipe",
        "display_name": "MaskDetailer (pipe)",
        "description": "",
        "python_module": "custom_nodes.ComfyUI-Impact-Pack",
        "category": "ImpactPack/Detailer",
        "output_node": false
    },
    "LoadImage": {
        "input": {
            "required": {
                "image": [
                    [
                        "example.png",
                        "clean.png",
                        "cleaned.png",
                        "default.png"
                    ],
                    {
                        "image_upload": true
                    }
                ]
            }
        },
        "input_order": {
            "required": [
                "image"
            ]
        },
        "output": [
            "IMAGE",
            "MASK"
        ],
        "output_is_list": [
            false,
            false
        ],
        "output_name": [
            "IMAGE",
            "MASK"
        ],
        "name": "LoadImage",
        "display_name": "Load Image",
        "description": "",
        "python_module": "nodes",
        "category": "image",
        "output_node": false
    }
}"""

WORKFLOW_JSON = """
{
  "id": "422469e4-5e00-4660-a5fe-911e1406a706",
  "revision": 0,
  "last_node_id": 2,
  "last_link_id": 2,
  "nodes": [
    {
      "id": 2,
      "type": "LoadImage",
      "pos": [
        -20230,
        -3250
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
          "links": [
            2
          ]
        }
      ],
      "properties": {
        "Node name for S&R": "LoadImage"
      },
      "widgets_values": [
        "example.png",
        "image"
      ]
    },
    {
      "id": 1,
      "type": "MaskDetailerPipe",
      "pos": [
        -19760,
        -3250
      ],
      "size": [
        365.208984375,
        638
      ],
      "flags": {},
      "order": 1,
      "mode": 0,
      "inputs": [
        {
          "name": "image",
          "type": "IMAGE",
          "link": 1
        },
        {
          "name": "mask",
          "type": "MASK",
          "link": 2
        },
        {
          "name": "basic_pipe",
          "type": "BASIC_PIPE",
          "link": null
        },
        {
          "name": "refiner_basic_pipe_opt",
          "shape": 7,
          "type": "BASIC_PIPE",
          "link": null
        },
        {
          "name": "detailer_hook",
          "shape": 7,
          "type": "DETAILER_HOOK",
          "link": null
        },
        {
          "name": "scheduler_func_opt",
          "shape": 7,
          "type": "SCHEDULER_FUNC",
          "link": null
        }
      ],
      "outputs": [
        {
          "name": "image",
          "type": "IMAGE",
          "links": null
        },
        {
          "name": "cropped_refined",
          "shape": 6,
          "type": "IMAGE",
          "links": null
        },
        {
          "name": "cropped_enhanced_alpha",
          "shape": 6,
          "type": "IMAGE",
          "links": null
        },
        {
          "name": "basic_pipe",
          "type": "BASIC_PIPE",
          "links": null
        },
        {
          "name": "refiner_basic_pipe_opt",
          "type": "BASIC_PIPE",
          "links": null
        }
      ],
      "properties": {
        "Node name for S&R": "MaskDetailerPipe"
      },
      "widgets_values": [
        512,
        true,
        1024,
        true,
        0,
        "randomize",
        20,
        8,
        "euler",
        "normal",
        0.5,
        5,
        3,
        10,
        0.2,
        1,
        1,
        false,
        20,
        false,
        true
      ]
    }
  ],
  "links": [
    [
      1,
      2,
      0,
      1,
      0,
      "IMAGE"
    ],
    [
      2,
      2,
      1,
      1,
      1,
      "MASK"
    ]
  ],
  "groups": [],
  "config": {},
  "extra": {
    "ds": {
      "scale": 1.6105100000000008,
      "offset": [
        20581.041071801712,
        3406.167811412577
      ]
    },
    "frontendVersion": "1.24.0-1"
  },
  "version": 0.4
}
"""




@pytest.fixture
def normalized_node_definitions():
    return Comfy_v1_0_NodeDefinitions.model_validate_json(NODE_DEFINITIONS_JSON).to_normalized()

@pytest.fixture
def workflow(normalized_node_definitions):
    return Comfy_V0_4_Workflow.model_validate_json(WORKFLOW_JSON).to_normalized(normalized_node_definitions).to_common(normalized_node_definitions)
# name
# type
# value
# is_link

def test_node_definition(workflow: Workflow):
    assert workflow
    mask_detailer_node = workflow.get_nodes_by_title("MaskDetailer (pipe)")[0]
    image_input = mask_detailer_node.get_input_by_name('image')
    assert image_input
    assert image_input.name == 'image'
    assert image_input.type == 'IMAGE'
    assert image_input.is_link == True

    image_input = mask_detailer_node.get_input_by_name('image')
    assert image_input
    assert image_input.name == 'image'
    assert image_input.type == 'IMAGE'
    assert image_input.is_link == True

    mask_input = mask_detailer_node.get_input_by_name('mask')
    assert mask_input
    assert mask_input.name == 'mask'
    assert mask_input.type == 'MASK'
    assert mask_input.is_link == True

    guide_size_input = mask_detailer_node.get_input_by_name('guide_size')
    assert guide_size_input
    assert guide_size_input.name == 'guide_size'
    assert guide_size_input.type == 'FLOAT'
    assert guide_size_input.value == 512.0
    assert guide_size_input.is_link == False

    seed_input = mask_detailer_node.get_input_by_name('seed')
    assert seed_input
    assert seed_input.name == 'seed'
    assert seed_input.type == 'INT'
    assert seed_input.value == 0
    assert seed_input.is_link == False

    steps_input = mask_detailer_node.get_input_by_name('steps')
    assert steps_input
    assert steps_input.name == 'steps'
    assert steps_input.type == 'INT'
    assert steps_input.value == 20
    assert steps_input.is_link == False

    basic_pipe_input = mask_detailer_node.get_input_by_name('basic_pipe')
    assert basic_pipe_input == None

    refiner_basic_pipe_opt_input = mask_detailer_node.get_input_by_name('refiner_basic_pipe_opt')
    assert refiner_basic_pipe_opt_input == None