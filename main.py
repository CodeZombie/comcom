import json
# import asyncio
# import aiohttp

#from transformers.workflows import Workflow
# from comcom.comfy_ui.models.raw.workflow.version_0_4.workflow import ComfyWorkflow
# from comcom.comfy_ui.definition.node_definitions import NodeDefinitions
# from comcom.comfy_ui.api_graph.workflow import ApiWorkflow
#from transformers.workflow import Workflow

# with open('workflow.json', 'r') as file:
#     workflow = json.load(file)

# wrapped_workflow = {
#     "prompt": workflow
# }


# async def do_req(url, payload):
#     async with aiohttp.ClientSession() as session:
#         async with session.post(url, data=payload) as resp:
#             print(resp.status)
#             print(await resp.text())

# payload = json.dumps(wrapped_workflow).encode('utf-8')

# asyncio.run(do_req("http://127.0.0.1:8188/prompt", payload))

# Load definitions
# node_definitions = NodeDefinitions.model_validate_json(open('object_info.json').read())
# comfy_workflow = ComfyWorkflow.model_validate_json(open('simple_sub_x.json').read())
# api_workflow = ApiWorkflow.from_comfy_workflow(comfy_workflow, node_definitions)
# print(api_workflow)


# from comcom.comfy_ui.models.raw.workflow.version_0_4.workflow import Comfy_V0_4_Workflow
# from comcom.comfy_ui.models.normalized.workflow.workflow import NormalizedWorkflow
# from comcom.comfy_ui.models.normalized.workflow.subgraph_definition import NormalizedSubgraphDefinition
# from comcom.comfy_ui.models.raw.node_definitions.version_1_0.node_definitions import Comfy_v1_0_NodeDefinitions

# WORKFLOW_WITH_SIMPLE_SUBGRAPH_JSON = """
# {
#   "id": "02439884-a1c5-449e-bf43-6e05377a45ca",
#   "revision": 0,
#   "last_node_id": 4,
#   "last_link_id": 4,
#   "nodes": [
#     {
#       "id": 1,
#       "type": "LoadImage",
#       "pos": [
#         367.3896789550781,
#         405.6490783691406
#       ],
#       "size": [
#         274.080078125,
#         314
#       ],
#       "flags": {},
#       "order": 0,
#       "mode": 0,
#       "inputs": [],
#       "outputs": [
#         {
#           "name": "IMAGE",
#           "type": "IMAGE",
#           "links": [
#             3
#           ]
#         },
#         {
#           "name": "MASK",
#           "type": "MASK",
#           "links": null
#         }
#       ],
#       "properties": {
#         "Node name for S&R": "LoadImage"
#       },
#       "widgets_values": [
#         "ComfyUI_00033_.png",
#         "image"
#       ]
#     },
#     {
#       "id": 3,
#       "type": "PreviewImage",
#       "pos": [
#         1297.4132080078125,
#         463.23114013671875
#       ],
#       "size": [
#         140,
#         26
#       ],
#       "flags": {},
#       "order": 2,
#       "mode": 0,
#       "inputs": [
#         {
#           "name": "images",
#           "type": "IMAGE",
#           "link": 4
#         }
#       ],
#       "outputs": [],
#       "properties": {
#         "Node name for S&R": "PreviewImage"
#       }
#     },
#     {
#       "id": 4,
#       "type": "958f4d94-38a9-4ed2-9e09-2de399857e0c",
#       "pos": [
#         932.72509765625,
#         458.424560546875
#       ],
#       "size": [
#         140,
#         26
#       ],
#       "flags": {},
#       "order": 1,
#       "mode": 0,
#       "inputs": [
#         {
#           "name": "image",
#           "type": "IMAGE",
#           "link": 3
#         }
#       ],
#       "outputs": [
#         {
#           "name": "IMAGE",
#           "type": "IMAGE",
#           "links": [
#             4
#           ]
#         }
#       ],
#       "properties": {},
#       "widgets_values": []
#     }
#   ],
#   "links": [
#     [
#       3,
#       1,
#       0,
#       4,
#       0,
#       "IMAGE"
#     ],
#     [
#       4,
#       4,
#       0,
#       3,
#       0,
#       "IMAGE"
#     ]
#   ],
#   "groups": [],
#   "definitions": {
#     "subgraphs": [
#       {
#         "id": "958f4d94-38a9-4ed2-9e09-2de399857e0c",
#         "version": 1,
#         "state": {
#           "lastGroupId": 0,
#           "lastNodeId": 3,
#           "lastLinkId": 2,
#           "lastRerouteId": 0
#         },
#         "revision": 0,
#         "config": {},
#         "name": "New Subgraph",
#         "inputNode": {
#           "id": -10,
#           "bounding": [
#             690.6282958984375,
#             441.42457580566406,
#             120,
#             60
#           ]
#         },
#         "outputNode": {
#           "id": -20,
#           "bounding": [
#             1200.6282958984375,
#             441.42457580566406,
#             120,
#             60
#           ]
#         },
#         "inputs": [
#           {
#             "id": "27aaa1f9-e12a-405e-bb6b-c49543d3b82b",
#             "name": "image",
#             "type": "IMAGE",
#             "linkIds": [
#               1
#             ],
#             "localized_name": "image",
#             "pos": {
#               "0": 55,
#               "1": 20
#             }
#           }
#         ],
#         "outputs": [
#           {
#             "id": "77c545ac-15ba-49d6-936e-ee706be7347b",
#             "name": "IMAGE",
#             "type": "IMAGE",
#             "linkIds": [
#               2
#             ],
#             "localized_name": "IMAGE",
#             "pos": {
#               "0": 20,
#               "1": 20
#             }
#           }
#         ],
#         "widgets": [],
#         "nodes": [
#           {
#             "id": 2,
#             "type": "ImageRotate",
#             "pos": [
#               870.6282958984375,
#               457.4245910644531
#             ],
#             "size": [
#               270,
#               58
#             ],
#             "flags": {},
#             "order": 0,
#             "mode": 0,
#             "inputs": [
#               {
#                 "localized_name": "image",
#                 "name": "image",
#                 "type": "IMAGE",
#                 "link": 1
#               }
#             ],
#             "outputs": [
#               {
#                 "localized_name": "IMAGE",
#                 "name": "IMAGE",
#                 "type": "IMAGE",
#                 "links": [
#                   2
#                 ]
#               }
#             ],
#             "properties": {
#               "Node name for S&R": "ImageRotate"
#             },
#             "widgets_values": [
#               "none"
#             ]
#           }
#         ],
#         "groups": [],
#         "links": [
#           {
#             "id": 1,
#             "origin_id": -10,
#             "origin_slot": 0,
#             "target_id": 2,
#             "target_slot": 0,
#             "type": "IMAGE"
#           },
#           {
#             "id": 2,
#             "origin_id": 2,
#             "origin_slot": 0,
#             "target_id": -20,
#             "target_slot": 0,
#             "type": "IMAGE"
#           }
#         ],
#         "extra": {}
#       }
#     ]
#   },
#   "config": {},
#   "extra": {
#     "ds": {
#       "scale": 1.3777431100456294,
#       "offset": [
#         -40.7685658938395,
#         -50.7207784300051
#       ]
#     },
#     "frontendVersion": "1.24.0-1"
#   },
#   "version": 0.4
# }
# """

# normalized_node_definitions = Comfy_v1_0_NodeDefinitions.model_validate_json(open('tests/data/object_info.json').read()).to_normalized()
# workflow = Comfy_V0_4_Workflow.model_validate_json(WORKFLOW_WITH_SIMPLE_SUBGRAPH_JSON).to_normalized(normalized_node_definitions).to_common(normalized_node_definitions)
# print(workflow)
# print(workflow.as_api_dict())
# print("---")
# print(workflow.as_json())


from comcom.playbook.playbook import Playbook
import yaml
from comcom.comfy_ui.models.raw.node_definitions.version_1_0.node_definitions import Comfy_v1_0_NodeDefinitions

normalized_node_definitions = Comfy_v1_0_NodeDefinitions.model_validate_json(open('tests/data/object_info.json').read()).to_normalized()

#playbook_dict = yaml.load(open('chargen/generate_character.yaml'), Loader=yaml.FullLoader)
playbook = Playbook.from_dict(playbook_dict)
workflow = playbook.get_workflow_by_path_str('generate_base_image')
workflow.execute(normalized_node_definitions)

#playbook.print('generate_base_image')




