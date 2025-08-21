import json
import pytest

from comcom.transformers.workflows import Node, NodeDefinition, Link, Workflow

ONE_NODE_MUTED_ALL_HOOKED_UP_WORKFLOW_JSON = """
{
  "id": "64a4f5af-8829-4df6-9262-8c8823035a68",
  "revision": 0,
  "last_node_id": 6,
  "last_link_id": 4,
  "nodes": [
    {
      "id": 1,
      "type": "LoadImage",
      "pos": [
        210,
        -40
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
          "links": null
        }
      ],
      "properties": {
        "Node name for S&R": "LoadImage"
      },
      "widgets_values": [
        "image.png",
        "image"
      ]
    },
    {
      "id": 3,
      "type": "LoadImage",
      "pos": [
        200,
        350
      ],
      "size": [
        274.080078125,
        314
      ],
      "flags": {},
      "order": 1,
      "mode": 0,
      "inputs": [],
      "outputs": [
        {
          "name": "IMAGE",
          "type": "IMAGE",
          "links": [
            2
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
        "image.png",
        "image"
      ]
    },
    {
      "id": 6,
      "type": "PreviewImage",
      "pos": [
        1090,
        320
      ],
      "size": [
        140,
        246
      ],
      "flags": {},
      "order": 4,
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
      "id": 5,
      "type": "PreviewImage",
      "pos": [
        1090,
        20
      ],
      "size": [
        140,
        246
      ],
      "flags": {},
      "order": 3,
      "mode": 0,
      "inputs": [
        {
          "name": "images",
          "type": "IMAGE",
          "link": 3
        }
      ],
      "outputs": [],
      "properties": {
        "Node name for S&R": "PreviewImage"
      },
      "widgets_values": []
    },
    {
      "id": 2,
      "type": "Image Paste Crop by Location",
      "pos": [
        630,
        280
      ],
      "size": [
        288.2300720214844,
        198
      ],
      "flags": {},
      "order": 2,
      "mode": 4,
      "inputs": [
        {
          "name": "image",
          "type": "IMAGE",
          "link": 1
        },
        {
          "name": "crop_image",
          "type": "IMAGE",
          "link": 2
        }
      ],
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
          "type": "IMAGE",
          "links": [
            4
          ]
        }
      ],
      "properties": {
        "Node name for S&R": "Image Paste Crop by Location"
      },
      "widgets_values": [
        0,
        0,
        256,
        256,
        0.25,
        0
      ]
    }
  ],
  "links": [
    [
      1,
      1,
      0,
      2,
      0,
      "IMAGE"
    ],
    [
      2,
      3,
      0,
      2,
      1,
      "IMAGE"
    ],
    [
      3,
      2,
      0,
      5,
      0,
      "IMAGE"
    ],
    [
      4,
      2,
      1,
      6,
      0,
      "IMAGE"
    ]
  ],
  "groups": [],
  "config": {},
  "extra": {
    "ds": {
      "scale": 1.1386306694591972,
      "offset": [
        365.51793125163704,
        197.03628966871887
      ]
    },
    "frontendVersion": "1.24.0-1"
  },
  "version": 0.4
}
"""

ONE_NODE_MUTED_FIRST_INPUT_MISSING_WORKFLOW_JSON = """
{
  "id": "64a4f5af-8829-4df6-9262-8c8823035a68",
  "revision": 0,
  "last_node_id": 6,
  "last_link_id": 6,
  "nodes": [
    {
      "id": 3,
      "type": "LoadImage",
      "pos": [
        200,
        350
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
            2
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
        "image.png",
        "image"
      ]
    },
    {
      "id": 1,
      "type": "LoadImage",
      "pos": [
        210,
        -40
      ],
      "size": [
        274.080078125,
        314
      ],
      "flags": {},
      "order": 1,
      "mode": 0,
      "inputs": [],
      "outputs": [
        {
          "name": "IMAGE",
          "type": "IMAGE",
          "links": []
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
        "image.png",
        "image"
      ]
    },
    {
      "id": 2,
      "type": "Image Paste Crop by Location",
      "pos": [
        630,
        280
      ],
      "size": [
        288.2300720214844,
        198
      ],
      "flags": {},
      "order": 2,
      "mode": 4,
      "inputs": [
        {
          "name": "image",
          "type": "IMAGE",
          "link": null
        },
        {
          "name": "crop_image",
          "type": "IMAGE",
          "link": 2
        }
      ],
      "outputs": [
        {
          "name": "IMAGE",
          "type": "IMAGE",
          "links": [
            6
          ]
        },
        {
          "name": "MASK",
          "type": "IMAGE",
          "links": [
            4
          ]
        }
      ],
      "properties": {
        "Node name for S&R": "Image Paste Crop by Location"
      },
      "widgets_values": [
        0,
        0,
        256,
        256,
        0.25,
        0
      ]
    },
    {
      "id": 5,
      "type": "PreviewImage",
      "pos": [
        1090,
        20
      ],
      "size": [
        140,
        246
      ],
      "flags": {},
      "order": 3,
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
      },
      "widgets_values": []
    },
    {
      "id": 6,
      "type": "PreviewImage",
      "pos": [
        1090,
        320
      ],
      "size": [
        140,
        246
      ],
      "flags": {},
      "order": 4,
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
    }
  ],
  "links": [
    [
      2,
      3,
      0,
      2,
      1,
      "IMAGE"
    ],
    [
      4,
      2,
      1,
      6,
      0,
      "IMAGE"
    ],
    [
      6,
      2,
      0,
      5,
      0,
      "IMAGE"
    ]
  ],
  "groups": [],
  "config": {},
  "extra": {
    "ds": {
      "scale": 1.5155174210501936,
      "offset": [
        26.887718067931218,
        164.0577785263934
      ]
    },
    "frontendVersion": "1.24.0-1"
  },
  "version": 0.4
}
"""

ONE_NODE_MUTED_LAST_INPUT_MISSING_FIRST_OUTPUT_MISSING_WORKFLOW_JSON = """
{
  "id": "64a4f5af-8829-4df6-9262-8c8823035a68",
  "revision": 0,
  "last_node_id": 6,
  "last_link_id": 7,
  "nodes": [
    {
      "id": 3,
      "type": "LoadImage",
      "pos": [
        200,
        350
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
          "links": []
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
        "image.png",
        "image"
      ]
    },
    {
      "id": 1,
      "type": "LoadImage",
      "pos": [
        210,
        -40
      ],
      "size": [
        274.080078125,
        314
      ],
      "flags": {},
      "order": 1,
      "mode": 0,
      "inputs": [],
      "outputs": [
        {
          "name": "IMAGE",
          "type": "IMAGE",
          "links": [
            7
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
        "image.png",
        "image"
      ]
    },
    {
      "id": 2,
      "type": "Image Paste Crop by Location",
      "pos": [
        630,
        280
      ],
      "size": [
        288.2300720214844,
        198
      ],
      "flags": {},
      "order": 3,
      "mode": 4,
      "inputs": [
        {
          "name": "image",
          "type": "IMAGE",
          "link": 7
        },
        {
          "name": "crop_image",
          "type": "IMAGE",
          "link": null
        }
      ],
      "outputs": [
        {
          "name": "IMAGE",
          "type": "IMAGE",
          "links": []
        },
        {
          "name": "MASK",
          "type": "IMAGE",
          "links": [
            4
          ]
        }
      ],
      "properties": {
        "Node name for S&R": "Image Paste Crop by Location"
      },
      "widgets_values": [
        0,
        0,
        256,
        256,
        0.25,
        0
      ]
    },
    {
      "id": 5,
      "type": "PreviewImage",
      "pos": [
        1090,
        20
      ],
      "size": [
        140,
        246
      ],
      "flags": {},
      "order": 2,
      "mode": 0,
      "inputs": [
        {
          "name": "images",
          "type": "IMAGE",
          "link": null
        }
      ],
      "outputs": [],
      "properties": {
        "Node name for S&R": "PreviewImage"
      },
      "widgets_values": []
    },
    {
      "id": 6,
      "type": "PreviewImage",
      "pos": [
        1090,
        320
      ],
      "size": [
        140,
        246
      ],
      "flags": {},
      "order": 4,
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
    }
  ],
  "links": [
    [
      4,
      2,
      1,
      6,
      0,
      "IMAGE"
    ],
    [
      7,
      1,
      0,
      2,
      0,
      "IMAGE"
    ]
  ],
  "groups": [],
  "config": {},
  "extra": {
    "ds": {
      "scale": 1.5155174210501936,
      "offset": [
        28.647226011797954,
        164.0577785263934
      ]
    },
    "frontendVersion": "1.24.0-1"
  },
  "version": 0.4
}
"""

@pytest.fixture
def node_definitions_dict():
    d = {}
    with open('tests/data/object_info.json', 'r') as f:
        d = json.load(f)
    return d

@pytest.fixture
def one_muted_all_hooked_workflow_dict():
    return json.loads(ONE_NODE_MUTED_ALL_HOOKED_UP_WORKFLOW_JSON)

@pytest.fixture
def one_muted_first_input_missing_workflow_dict():
    return json.loads(ONE_NODE_MUTED_FIRST_INPUT_MISSING_WORKFLOW_JSON)

@pytest.fixture
def one_node_muted_last_input_missing_first_output_missing_workflow_dict():
    return json.loads(ONE_NODE_MUTED_LAST_INPUT_MISSING_FIRST_OUTPUT_MISSING_WORKFLOW_JSON)

def test_all_hooked_up_workflow(one_muted_all_hooked_workflow_dict, node_definitions_dict):
    workflow = Workflow.from_workflow_json_dict(one_muted_all_hooked_workflow_dict, node_definitions_dict)

    load_image_node_a = workflow.get_node_by_id('1')
    load_image_node_b = workflow.get_node_by_id('3')
    preview_node_a = workflow.get_node_by_id('5')
    preview_node_b = workflow.get_node_by_id('6')

    assert preview_node_a.get_input('images').value.source_node_id == str(load_image_node_a.id)
    assert preview_node_a.get_input('images').value.source_output_id == 0

    assert preview_node_b.get_input('images').value.source_node_id == str(load_image_node_b.id)
    assert preview_node_b.get_input('images').value.source_output_id == 0

def test_first_input_missing_workflow(one_muted_first_input_missing_workflow_dict, node_definitions_dict):
    workflow = Workflow.from_workflow_json_dict(one_muted_first_input_missing_workflow_dict, node_definitions_dict)
    load_image_node_a = workflow.get_node_by_id('1')
    load_image_node_b = workflow.get_node_by_id('3')
    preview_node_a = workflow.get_node_by_id('5')
    preview_node_b = workflow.get_node_by_id('6')

    assert preview_node_a.get_input('images').value.source_node_id == None
    assert preview_node_a.get_input('images').value.source_output_id == None

    assert preview_node_b.get_input('images').value.source_node_id == str(load_image_node_b.id)
    assert preview_node_b.get_input('images').value.source_output_id == 0

def test_last_input_missing_first_output_missing(one_node_muted_last_input_missing_first_output_missing_workflow_dict, node_definitions_dict):
    workflow = Workflow.from_workflow_json_dict(one_node_muted_last_input_missing_first_output_missing_workflow_dict, node_definitions_dict)
    load_image_node_a = workflow.get_node_by_id('1')
    load_image_node_b = workflow.get_node_by_id('3')
    preview_node_a = workflow.get_node_by_id('5')
    preview_node_b = workflow.get_node_by_id('6')

    assert preview_node_a.get_input('images').value.source_node_id == None
    assert preview_node_a.get_input('images').value.source_output_id == None

    assert preview_node_b.get_input('images').value.source_node_id == None
    assert preview_node_b.get_input('images').value.source_output_id == None