import pytest

from typing import List, Dict

from comcom.comfy_ui.models.raw.node_definitions.version_1_0.node_definitions import Comfy_v1_0_NodeDefinitions


MASK_DETAILER_NODE_DEF = """
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
    }
}"""



@pytest.fixture
def node_definitions():
    return Comfy_v1_0_NodeDefinitions.model_validate_json(MASK_DETAILER_NODE_DEF)

def test_node_definition(node_definitions: Comfy_v1_0_NodeDefinitions):
    mask_detailer_pipe_node_def = node_definitions.get_node_definition('MaskDetailerPipe')
    assert len(mask_detailer_pipe_node_def.inputs) == 27
    seed_input_def = mask_detailer_pipe_node_def.get_input_definition('seed')
    assert seed_input_def.type == "INT"