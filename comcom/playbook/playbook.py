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

        workflows: Dict[str, WorkflowInstance] = {}
        workflow_dicts = playbook_dict.get('workflows', {})
        for workflow_id in workflow_dicts.keys():
            workflows[workflow_id] = WorkflowInstance.from_dict(workflow_dicts[workflow_id], {}, globals)

        return cls(
            globals=playbook_dict.get('globals', {}),
            workflows=workflows
        )
    
    @classmethod
    def get_node_definitions_dict_from_comfy_server(cls) -> Dict:
        pass

    def print(self, workflow_id: str):
        workflow = self.workflows.get(workflow_id, None)
        if workflow:
            return workflow.print(workflow_id)
        raise Exception("Workflow {} Not found".format(workflow_id))