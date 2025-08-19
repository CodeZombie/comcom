import pytest

from comcom.comfy_ui.definition.node_definitions import NodeDefinitions

@pytest.fixture
def node_definitions():
    return NodeDefinitions.model_validate_json(open('tests/data/object_info.json').read())

def test_node_definition(node_definitions):
    assert 'ImageStitch' in node_definitions.root.keys()
    
    assert node_definitions['ImageStitch']
    image_stitch_node_definition = node_definitions['ImageStitch']
    assert len(image_stitch_node_definition.inputs.keys()) == 6
    assert image_stitch_node_definition.inputs['image1'].type == "IMAGE"
    assert image_stitch_node_definition.inputs['direction'].type == "ENUM"
    assert image_stitch_node_definition.inputs['image2'].type == "IMAGE"

    image_only_checkpoint_loader_node_definition = node_definitions['ImageOnlyCheckpointLoader']
    assert image_only_checkpoint_loader_node_definition.inputs['ckpt_name'].type == "ENUM"

def test_virtual_input_definition(node_definitions):
    assert 'KSampler' in node_definitions.root.keys()
    ksampler_input_definition = node_definitions['KSampler']
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


