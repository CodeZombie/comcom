import json
# import asyncio
# import aiohttp

from transformers.workflows import Workflow
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


with open('simple_sub_x.json', 'r') as file:
    workflow = json.load(file)

with open('object_info.json', 'r') as file:
    node_definitions = json.load(file)

workflow = Workflow.from_workflow_json_dict(workflow, node_definitions)

print(workflow)

# print("WORKFLOW OBJ DATA")
# print(workflow)

# print("API PROMPT:")
with open('output_v02.json', 'w') as f:
    json.dump(workflow.to_api_prompt(), f)
