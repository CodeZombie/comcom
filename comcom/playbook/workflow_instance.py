from typing import Dict, Any, Self
from dataclasses import dataclass
from comcom.playbook.template_solver.template_dict_solver import TemplateDictSolver

class OutputMap:
    node: str
    filename: str

    @classmethod
    def from_dict(cls, output_map_dict: Dict) -> Self:
        return cls(
            node=output_map_dict.get('node'),
            filename=output_map_dict.get('filename')
        )
@dataclass
class WorkflowInstance:
    path: str
    values: Dict[str, str | int | float]
    input: Dict[str, str | int | float]
    output: Dict[str, OutputMap]
    workflows: Dict[str, Self]

    @classmethod
    def from_dict(cls, workflow_map_dict: Dict, parent_values: Dict, global_values: Dict) -> Self:
        path: str = workflow_map_dict.get('path')
        solved_values: Dict = TemplateDictSolver.solve(workflow_map_dict.get('values', {}), global_values | {'^': parent_values})
        solved_input: Dict = TemplateDictSolver.solve(workflow_map_dict.get('input', {}), global_values | solved_values | {'^': parent_values})
        solved_raw_output: Dict = TemplateDictSolver.solve(workflow_map_dict.get('output', {}), global_values | solved_values | {'^': parent_values})
        solved_outputs: Dict = {}

        for key in solved_raw_output.keys():
            solved_outputs[key] = OutputMap.from_dict(solved_raw_output[key])

        workflows: Dict[str, Self] = {}
        for child_workflow_key, child_workflow_dict in workflow_map_dict.get('workflows', {}).items():
            workflows[child_workflow_key] = cls.from_dict(child_workflow_dict, global_values | {'^': {solved_values | {'^': parent_values}}})
        
        return cls(
            path=path,
            values=solved_values,
            input=solved_input,
            output=solved_outputs,
            workflows=workflows
        )

    def execute(self):
        pass