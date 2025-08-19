import json
# import asyncio
# import aiohttp

#from transformers.workflows import Workflow
from comcom.comfy_ui.workflow_graph.workflow import ComfyWorkflow
from comcom.comfy_ui.definition.node_definitions import NodeDefinitions
from comcom.comfy_ui.api_graph.workflow import ApiWorkflow
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
node_definitions = NodeDefinitions.model_validate_json(open('object_info.json').read())
comfy_workflow = ComfyWorkflow.model_validate_json(open('simple_sub_x.json').read())
api_workflow = ApiWorkflow.from_comfy_workflow(comfy_workflow, node_definitions)
print(api_workflow)

