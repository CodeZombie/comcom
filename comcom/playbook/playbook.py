from typing import Dict, Any, Self, List
from dataclasses import dataclass
import os
import urllib.request
import functools

from .workflow_instance import WorkflowInstance
from comcom.playbook.template_solver.template_dict_solver import TemplateDictSolver
from comcom.comfy_ui.models.raw.node_definitions.version_1_0.node_definitions import Comfy_v1_0_NodeDefinitions
from comcom.comfy_ui.models.normalized.node_definition.node_definition import NormalizedNodeDefinition

from comcom.comfy_ui.server.server import ComfyServer

from .utils.dict_utils import flatten_dict

@dataclass
class Playbook:
    globals: Dict[str, Any]
    workflows: Dict[str, WorkflowInstance]

    @classmethod
    def from_dict(cls, playbook_dict: Dict) -> Self:
        globals: Dict[str, Any] = TemplateDictSolver.solve(playbook_dict.get('globals', {}))

        workflows: Dict[str, WorkflowInstance] = {}
        workflow_dicts = playbook_dict.get('workflows', {})
        for workflow_id in workflow_dicts.keys():
            workflows[workflow_id] = WorkflowInstance.from_dict(workflow_id, workflow_dicts[workflow_id], {}, globals)

        return cls(
            globals=playbook_dict.get('globals', {}),
            workflows=workflows
        )
    

    def get_flattened_workflows(self):
        flattened_dict = self.workflows.copy()
        for workflow_id, workflow in self.workflows.items():
            nested_workflows = workflow.get_flattened_children()
            for key, value in nested_workflows.items():
                flattened_dict["{}.{}".format(workflow_id, key)] = value
        return flattened_dict
    
    @property
    def workflow_names(self) -> List[str]:
        return list(self.get_flattened_workflows().keys())
    
    def get_workflow_by_path(self, workflow_path: str | List[str]) -> WorkflowInstance | None:
        if isinstance(workflow_path, str):
            workflow_path = workflow_path.split('.')

        if len(workflow_path) == 0:
            return None
        
        for id, workflow in self.workflows.items():
            if id == workflow_path[0]:
                if len(workflow_path) == 1:
                    return workflow
                return workflow.get_workflow_by_path(workflow_path[1:])
        return None
    
    def execute_workflow(self, workflow_path: str, comfy_server: ComfyServer):
        workflow = self.get_workflow_by_path(workflow_path)
        server_to_local_map = workflow.execute(comfy_server)
        for server_url, local_uri in server_to_local_map.items():
            print("{} -> {}".format(server_url, local_uri))
            # Download the data from server_url and save it as a PNG file at local_uri
            # TODO: maybe we do this in the Workflow Instance???
            request = urllib.request.Request(server_url)
            real_local_uri = os.path.abspath("{}.png".format(local_uri))
            os.makedirs(os.path.dirname(real_local_uri), exist_ok=True)
            with open(real_local_uri, 'wb') as f:
                f.write(urllib.request.urlopen(request).read())
            print("Saved.")
        
    def print(self, workflow_id: str):
        workflow = self.workflows.get(workflow_id, None)
        if workflow:
            return workflow.print(workflow_id)
        raise Exception("Workflow {} Not found".format(workflow_id))