import pytest

from comcom.comfy_ui.models.raw.workflow.version_0_4.workflow import Comfy_V0_4_Workflow
from comcom.comfy_ui.models.normalized.workflow.workflow import NormalizedWorkflow
from comcom.comfy_ui.models.normalized.workflow.subgraph_definition import NormalizedSubgraphDefinition
from comcom.comfy_ui.models.raw.node_definitions.version_1_0.node_definitions import Comfy_v1_0_NodeDefinitions

WORKFLOW_WITH_REROUTES_JSON = """
{
  "id": "a5e3cb68-0794-4ed8-b55b-2af84eb5fac9",
  "revision": 0,
  "last_node_id": 6,
  "last_link_id": 7,
  "nodes": [
    {
      "id": 3,
      "type": "Reroute",
      "pos": [
        751.4545288085938,
        360.6692810058594
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
          "widget": {
            "name": "value"
          },
          "link": 1
        }
      ],
      "outputs": [
        {
          "name": "",
          "type": "INT",
          "links": [
            2
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
        842.5838012695312,
        553.853515625
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
          "widget": {
            "name": "value"
          },
          "link": 6
        }
      ],
      "outputs": [
        {
          "name": "",
          "type": "INT",
          "links": [
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
      "id": 5,
      "type": "Reroute",
      "pos": [
        704.7724609375,
        575.2078247070312
      ],
      "size": [
        75,
        26
      ],
      "flags": {},
      "order": 3,
      "mode": 0,
      "inputs": [
        {
          "name": "",
          "type": "*",
          "widget": {
            "name": "value"
          },
          "link": 5
        }
      ],
      "outputs": [
        {
          "name": "",
          "type": "INT",
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
      "id": 4,
      "type": "Reroute",
      "pos": [
        591.5438232421875,
        540.9413452148438
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
          "widget": {
            "name": "value"
          },
          "link": 4
        }
      ],
      "outputs": [
        {
          "name": "",
          "type": "INT",
          "links": [
            5
          ]
        }
      ],
      "properties": {
        "showOutputText": false,
        "horizontal": false
      }
    },
    {
      "id": 2,
      "type": "GetImageSize",
      "pos": [
        500.4144592285156,
        381.5272521972656
      ],
      "size": [
        140,
        66
      ],
      "flags": {},
      "order": 0,
      "mode": 0,
      "inputs": [
        {
          "name": "image",
          "type": "IMAGE",
          "link": null
        }
      ],
      "outputs": [
        {
          "name": "width",
          "type": "INT",
          "links": [
            1
          ]
        },
        {
          "name": "height",
          "type": "INT",
          "links": [
            3
          ]
        },
        {
          "name": "batch_size",
          "type": "INT",
          "links": [
            4
          ]
        }
      ],
      "properties": {
        "Node name for S&R": "GetImageSize"
      }
    },
    {
      "id": 1,
      "type": "EmptyLatentImage",
      "pos": [
        946.3768310546875,
        378.2991027832031
      ],
      "size": [
        270,
        106
      ],
      "flags": {},
      "order": 5,
      "mode": 0,
      "inputs": [
        {
          "name": "width",
          "type": "INT",
          "widget": {
            "name": "width"
          },
          "link": 2
        },
        {
          "name": "height",
          "type": "INT",
          "widget": {
            "name": "height"
          },
          "link": 3
        },
        {
          "name": "batch_size",
          "type": "INT",
          "widget": {
            "name": "batch_size"
          },
          "link": 7
        }
      ],
      "outputs": [
        {
          "name": "LATENT",
          "type": "LATENT",
          "links": null
        }
      ],
      "properties": {
        "Node name for S&R": "EmptyLatentImage"
      },
      "widgets_values": [
        512,
        512,
        1
      ]
    }
  ],
  "links": [
    [
      1,
      2,
      0,
      3,
      0,
      "*"
    ],
    [
      2,
      3,
      0,
      1,
      0,
      "INT"
    ],
    [
      3,
      2,
      1,
      1,
      1,
      "INT"
    ],
    [
      4,
      2,
      2,
      4,
      0,
      "*"
    ],
    [
      5,
      4,
      0,
      5,
      0,
      "*"
    ],
    [
      6,
      5,
      0,
      6,
      0,
      "*"
    ],
    [
      7,
      6,
      0,
      1,
      2,
      "INT"
    ]
  ],
  "groups": [],
  "config": {},
  "extra": {
    "ds": {
      "scale": 2.6848315579531,
      "offset": [
        -364.3414323603506,
        -154.94563140016942
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
    return Comfy_V0_4_Workflow.model_validate_json(WORKFLOW_WITH_REROUTES_JSON).to_normalized(normalized_node_definitions).to_common(normalized_node_definitions)

def test_workflow_properties(workflow):
    assert workflow.id == "a5e3cb68-0794-4ed8-b55b-2af84eb5fac9"
    assert len(workflow.nodes) == 2
    get_image_size_node = workflow.get_node_by_id('2')
    assert get_image_size_node
    assert get_image_size_node.id == '2'
    assert get_image_size_node.get_input_by_name('image')
    assert get_image_size_node.get_input_by_name('image').name == 'image'
    assert get_image_size_node.get_input_by_name('image').is_link == True
    assert get_image_size_node.get_input_by_name('image').value.source_node_id == None
    assert get_image_size_node.get_input_by_name('image').value.source_node_output_name == None

    empty_image_node = workflow.get_node_by_id('1')
    assert empty_image_node
    assert empty_image_node.id == '1'
    assert empty_image_node.get_input_by_name('width')
    assert empty_image_node.get_input_by_name('width').name == 'width'
    assert empty_image_node.get_input_by_name('width').is_link == True
    assert empty_image_node.get_input_by_name('width').value.source_node_id == '2'
    assert empty_image_node.get_input_by_name('width').value.source_node_output_name == 'width'

    assert empty_image_node.get_input_by_name('height')
    assert empty_image_node.get_input_by_name('height').name == 'height'
    assert empty_image_node.get_input_by_name('height').is_link == True
    assert empty_image_node.get_input_by_name('height').value.source_node_id == '2'
    assert empty_image_node.get_input_by_name('height').value.source_node_output_name == 'height'

    assert empty_image_node.get_input_by_name('batch_size')
    assert empty_image_node.get_input_by_name('batch_size').name == 'batch_size'
    assert empty_image_node.get_input_by_name('batch_size').is_link == True
    assert empty_image_node.get_input_by_name('batch_size').value.source_node_id == '2'
    assert empty_image_node.get_input_by_name('batch_size').value.source_node_output_name == 'batch_size'
