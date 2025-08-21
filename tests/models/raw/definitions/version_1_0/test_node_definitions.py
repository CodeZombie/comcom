import pytest

from typing import List, Dict

from comcom.comfy_ui.models.raw.node_definitions.version_1_0.node_definitions import Comfy_v1_0_NodeDefinitions

@pytest.fixture
def node_definitions():
    return Comfy_v1_0_NodeDefinitions.model_validate_json(open('tests/data/object_info.json').read())

def test_node_definition(node_definitions: Comfy_v1_0_NodeDefinitions):

    image_stitch_node_definition = node_definitions.get_node_definition('ImageStitch')
    assert image_stitch_node_definition
    assert image_stitch_node_definition.name == "ImageStitch"
    assert len(image_stitch_node_definition.inputs) == 6

    

    assert image_stitch_node_definition.inputs['image1'].type == "IMAGE"
    assert image_stitch_node_definition.inputs['direction'].type == "ENUM"
    assert image_stitch_node_definition.inputs['image2'].type == "IMAGE"

    image_only_checkpoint_loader_node_definition = node_definitions.get_node_definition('ImageOnlyCheckpointLoader')
    assert image_only_checkpoint_loader_node_definition.inputs['ckpt_name'].type == "ENUM"

def test_virtual_input_definition(node_definitions):
    assert node_definitions.get_node_definition('KSampler')
    ksampler_input_definition = node_definitions.get_node_definition('KSampler')
    input_names = [
        "model",
        "seed",
        "control_after_generate", # Virtual input
        "steps",
        "cfg",
        "sampler_name",
        "scheduler",
        "positive",
        "negative",
        "latent_image",
        "denoise",
        ]
    
    for index, name in enumerate(ksampler_input_definition.inputs.keys()):
        assert name == input_names[index]


