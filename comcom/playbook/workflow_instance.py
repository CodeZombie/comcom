from typing import Dict, Any, Self
from dataclasses import dataclass
from comcom.playbook.utils.dict_utils import flatten_dict
from comcom.playbook.template_solver.template_dict_solver import TemplateDictSolver

@dataclass
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

    # TODO: children should be able to access their parent's `input` and `output` values in the dot dict.

    @classmethod
    def from_dict(cls, workflow_map_dict: Dict, parent_values: Dict, global_values: Dict) -> Self:
        path: str = workflow_map_dict.get('path', None)
        solved_values: Dict = TemplateDictSolver.solve(workflow_map_dict.get('values', {}), global_values | {'^': parent_values})
        solved_input: Dict = TemplateDictSolver.solve(workflow_map_dict.get('input', {}), global_values | solved_values | {'^': parent_values})
        solved_raw_output: Dict = TemplateDictSolver.solve(workflow_map_dict.get('output', {}), global_values | solved_values | {'^': parent_values})
        solved_outputs: Dict = {}

        for key in solved_raw_output.keys():
            solved_outputs[key] = OutputMap.from_dict(solved_raw_output[key])

        workflows: Dict[str, Self] = {}
        for child_workflow_key, child_workflow_dict in workflow_map_dict.get('workflows', {}).items():
            workflows[child_workflow_key] = cls.from_dict(child_workflow_dict, solved_values | {'^': parent_values } | {'input': solved_input} | {'output': solved_outputs}, global_values)
        
        return cls(
            path=path,
            values=solved_values,
            input=solved_input,
            output=solved_outputs,
            workflows=workflows
        )

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

    