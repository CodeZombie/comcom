from typing import Dict, Any, Self, List
from dataclasses import dataclass
from .workflow_instance import WorkflowInstance
from comcom.playbook.template_solver.template_dict_solver import TemplateDictSolver

@dataclass
class Playbook:
    globals: Dict[str, Any]
    workflows: Dict[str, WorkflowInstance]

    @classmethod
    def from_dict(cls, playbook_dict: Dict) -> Self:
        globals: Dict[str, Any] = TemplateDictSolver.solve(playbook_dict.get('globals', {}))

        workflow_instances: Dict[str, WorkflowInstance]
        workflow_instance_dicts = playbook_dict.get('workflows', {})
        for workflow_id in workflow_instance_dicts.keys():
            workflow_instances[workflow_id] = WorkflowInstance.from_dict(workflow_instance_dicts[workflow_id])

        return cls(
            globals=playbook_dict.get('globals', {}),
        )
    
    @classmethod
    def get_node_definitions_dict_from_comfy_server(cls) -> Dict:
        pass

    def resolve_inputs(): 
        pass