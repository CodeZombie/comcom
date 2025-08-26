from typing import Dict, Any, Self, List
from dataclasses import dataclass
import json
import os
import uuid
import websocket
import urllib
import urllib.request
from comcom.playbook.utils.dict_utils import flatten_dict
from comcom.playbook.template_solver.template_dict_solver import TemplateDictSolver

from comcom.comfy_ui.models.raw.workflow.version_0_4.workflow import Comfy_V0_4_Workflow
from comcom.comfy_ui.models.normalized.node_definition.node_definition import NormalizedNodeDefinition

from comcom.comfy_ui.models.raw.node_definitions.version_1_0.node_definitions import Comfy_v1_0_NodeDefinitions

from comcom.comfy_ui.models.common.workflow import Workflow

from comcom.comfy_ui.server.server import ComfyServer

# @dataclass
# class OutputMap:
#     node: str
#     filename: str

#     @classmethod
#     def from_dict(cls, output_map_dict: Dict) -> Self:
#         return cls(
#             node=output_map_dict.get('node'),
#             filename=output_map_dict.get('filename')
#         )
@dataclass
class WorkflowInstance:
    id: str
    path: str
    values: Dict[str, str | int | float]
    input: Dict[str, str | int | float]
    output: Dict[str, str]
    workflows: Dict[str, Self]

    # TODO: children should be able to access their parent's `input` and `output` values in the dot dict.

    @classmethod
    def from_dict(cls, id: str, workflow_map_dict: Dict, parent_values: Dict, global_values: Dict) -> Self:
        id: str = id
        path: str = workflow_map_dict.get('path', None)
        solved_values: Dict = TemplateDictSolver.solve(workflow_map_dict.get('values', {}), global_values | {'^': parent_values})
        solved_input: Dict = TemplateDictSolver.solve(workflow_map_dict.get('input', {}), global_values | solved_values | {'^': parent_values})
        solved_raw_output: Dict = TemplateDictSolver.solve(workflow_map_dict.get('output', {}), global_values | solved_values | {'^': parent_values})
        solved_outputs: Dict = {}

        for key in solved_raw_output.keys():
            solved_outputs[key] = solved_raw_output[key]

        workflows: Dict[str, Self] = {}
        for child_workflow_key, child_workflow_dict in workflow_map_dict.get('workflows', {}).items():
            workflows[child_workflow_key] = cls.from_dict(child_workflow_key, child_workflow_dict, solved_values | {'^': parent_values } | {'input': solved_input} | {'output': solved_outputs}, global_values)
        
        return cls(
            id=id,
            path=path,
            values=solved_values,
            input=solved_input,
            output=solved_outputs,
            workflows=workflows
        )
    
    def to_api_dict(self, node_definitions: List[NormalizedNodeDefinition]) -> Dict:
        comfy_workflow = Comfy_V0_4_Workflow.model_validate_json(open(os.path.join('workflows', self.path)).read()).to_normalized(node_definitions).to_common(node_definitions)
        
        for key, value in flatten_dict(self.input).items():
            input_path = key.rsplit('.', 1)
            if len(input_path) != 2:
                raise Exception("Workflow \"{workflow_id}\"'s input \"{input_path}\" is invalid. Must be formatted like \"<node>.<input_name>\", not whatever that is.".format(workflow_id=self.id, input_path=key))
            node_identifier = input_path[0]
            input_identifier = input_path[1]
            # If the node identifier starts with a $, we want to search by ID
            nodes = []
            if node_identifier.startswith('$'):
                node = comfy_workflow.get_node_by_id(node_identifier[1:])
                if node:
                    nodes.append(node)
            # If we haven't found a node, let's try searching by title.
            # This will allow us to match nodes that have a `$` at the beginning of the title.
            if not nodes:
                nodes = comfy_workflow.get_nodes_by_title(node_identifier)
                if len(nodes) > 1:
                    print("WARNING: more than one node has the title {}. We're going to apply modifications to all of them. Be sure that this is what you want.".format(node_identifier))
            if not nodes:
                print("Could not find a node for identifier {}".format(node_identifier))
            for node in nodes:
                input = node.get_input_by_name(input_identifier)

                if not input:
                    raise Exception('Node \"{node_title}\" (identified by \"{node_identifier}\") <type={node_type}> does not have an input called {input_identifier}. Available inputs are: {available_inputs}'.format(
                        node_title=node.title,
                        node_identifier=node_identifier,
                        node_type=node.type,
                        input_identifier=input_identifier,
                        available_inputs=[input.name for input in node.inputs if not input.is_link]
                        ))
                input.value = value
        return comfy_workflow.as_api_dict()
    

    # comfy_server = ComfyServer('127.0.0.1', 8188)
    # def execute(self, comfy_server: ComfyServer, on_node_progress: Callable) -> Dict[str, str]:
    #     node_definitions = Comfy_v1_0_NodeDefinitions.model_validate(comfy_server.get_node_definitions_dict()).to_normalized()
    #     comfy_workflow = Comfy_V0_4_Workflow.model_validate_json(open(os.path.join('workflows', self.path)).read()).to_normalized(node_definitions).to_common(node_definitions)
        
    #     for key, value in flatten_dict(self.input).items():
    #         input_path = key.rsplit('.', 1)
    #         if len(input_path) != 2:
    #             raise Exception("Workflow \"{workflow_id}\"'s input \"{input_path}\" is invalid. Must be formatted like \"<node>.<input_name>\", not whatever that is.".format(workflow_id=self.id, input_path=key))
    #         node_identifier = input_path[0]
    #         input_identifier = input_path[1]
    #         # If the node identifier starts with a $, we want to search by ID
    #         nodes = []
    #         if node_identifier.startswith('$'):
    #             node = comfy_workflow.get_node_by_id(node_identifier[1:])
    #             if node:
    #                 nodes.append(node)
    #         # If we haven't found a node, let's try searching by title.
    #         # This will allow us to match nodes that have a `$` at the beginning of the title.
    #         if not nodes:
    #             nodes = comfy_workflow.get_nodes_by_title(node_identifier)
    #             if len(nodes) > 1:
    #                 print("WARNING: more than one node has the title {}. We're going to apply modifications to all of them. Be sure that this is what you want.".format(node_identifier))
    #         if not nodes:
    #             print("Could not find a node for identifier {}".format(node_identifier))
    #         for node in nodes:
    #             input = node.get_input_by_name(input_identifier)

    #             if not input:
    #                 raise Exception('Node \"{node_title}\" (identified by \"{node_identifier}\") <type={node_type}> does not have an input called {input_identifier}. Available inputs are: {available_inputs}'.format(
    #                     node_title=node.title,
    #                     node_identifier=node_identifier,
    #                     node_type=node.type,
    #                     input_identifier=input_identifier,
    #                     available_inputs=[input.name for input in node.inputs if not input.is_link]
    #                     ))
    #             input.value = value
    #     return comfy_workflow.as_api_dict()
        #print("Executing workflow \"{}\"".format(comfy_workflow.id))

        # node_outputs = comfy_server.submit_workflow_instance(comfy_workflow)
        # output_map = {}
        # for node_id, server_filepath in node_outputs.items():
        #     node_tile = comfy_workflow.get_node_by_id(node_id).title
        #     if "${}".format(node_id) in self.output.keys():
        #         output_map[server_filepath] = self.output["${}".format(node_id)]
        #     elif node_tile in self.output.keys():
        #         output_map[server_filepath] = self.output[node_tile]
        #     else:
        #         print(f"WARNING: output node {node_id} ({node_tile}) does not contain a matching key in playbook. This output will not be saved.")
        # return output_map

        # client_id = str(uuid.uuid4())
        # ws = websocket.WebSocket()
        # ws.connect(f"ws://127.0.0.1:8188/ws?clientId={client_id}")
        # prompt_dict = {
        #     'prompt': comfy_workflow.as_api_dict(),
        #     'client_id': client_id
        # }
        # prompt_json = json.dumps(prompt_dict).encode('utf-8')
        # req = urllib.request.Request(f'http://127.0.0.1:8188/prompt', data=prompt_json)
        # try:
        #     return_data = json.loads(urllib.request.urlopen(req).read())
        # except urllib.error.HTTPError as e:
        #     errors = []
        #     error_dict = json.loads(e.read())
        #     for node_id, node_error_dict in error_dict.get('node_errors', {}).items():
        #         for error in node_error_dict.get('errors', []):
        #             errors.append(
        #                 "Node {node_id} ({node_type}) failed with error \"{error_text}.\" [{extra}]".format(
        #                     node_id=node_id, 
        #                     node_type=node_error_dict.get('class_type', "Unknown node class type"),
        #                     error_text=error.get('details', "Unknown error"),
        #                     extra=error.get('extra_info', "")
        #                 )
        #             )
            
        #     for error in errors:
        #         print("Errors occurred validating prompt:")
        #         print("  {}".format(error))
            
        #     return
        # prompt_id = return_data['prompt_id']
        # print("generating...")
        # while True:
        #     out = ws.recv()
        #     if isinstance(out, str):
        #         message = json.loads(out)
        #         print(message)
        #         if message['type'] == 'executing':
        #             data = message['data']
        #             if data['node'] is None and data['prompt_id'] == prompt_id:
        #                 break
        #     else:
        #         continue
        # ws.close()
        
        # prompt_history = json.loads(urllib.request.urlopen(f"http://127.0.0.1:8188/history/{prompt_id}").read())[prompt_id]
        # for node_id in prompt_history['outputs']:
        #     node_output = prompt_history['outputs'][node_id]
        #     images_output = []
        #     if 'images' in node_output:
        #         for image in node_output['images']:
        #             image_url_data = urllib.parse.urlencode({"filename": image['filename'], "subfolder": image['subfolder'], "type": image['type']})
        #             print("IMAGE: ")
        #             print(f"http://127.0.0.1:8188/view?{image_url_data}")
                    

    def get_workflow_by_path(self, workflow_path: List[str]) -> Self | None:
        if len(workflow_path) == 0:
            return None
        for id, workflow in self.workflows.items():
            if id == workflow_path[0]:
                if len(workflow_path) == 1:
                    return workflow
                return workflow.get_workflow_by_path(workflow_path[1:])
        return None

    def get_flattened_children(self):
        flattened_dict = self.workflows.copy()
        for child_workflow in self.workflows.values():
            nested_workflows = child_workflow.get_flattened_children()
            for key, value in nested_workflows.items():
                flattened_dict["{}.{}".format(self.id, key)] = value
        return flattened_dict

    def print(self, id, prfx=""):
        print("{}{}".format(prfx, id))
        print("{}  path:".format(prfx))
        print("{}    {}".format(prfx, self.path))
        print("{}  values:".format(prfx))
        for key, value in flatten_dict(self.values).items():
            print("{}    {}: {}".format(prfx, key, value))
        print("{}  input:".format(prfx))
        for key, value in flatten_dict(self.input).items():
            print("{}    {}: {}".format(prfx, key, value))
        print("{}  output:".format(prfx, prfx))
        for key, value in flatten_dict(self.output).items():
            print("{}    {}: {}".format(prfx, key, value))
        print("{}  workflows: ".format(prfx, prfx))
        for key, value in self.workflows.items():
            value.print(key, prfx + "    ")
        #print("  Children: {}".format([workflow.path for workflow in self.workflows]))

    