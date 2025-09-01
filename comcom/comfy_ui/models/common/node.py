from typing import List, Self
from dataclasses import dataclass
from .input import Input
from .output import Output

@dataclass
class Node:
    id: str
    title: str
    type: str
    inputs: List[Input]
    outputs: List[Output]

    def get_input_by_name(self, name: str) -> Input:
        return next((input for input in self.inputs if input.name == name), None)
    
    def get_output_index_by_name(self, output_name: str) -> int:
        for output in self.outputs:
            if output.name == output_name:
                return output.index
        return None
    
    def as_api_dict(self, all_nodes: List[Self]):
        api_dict = dict()
        api_dict['class_type'] = self.type
        api_dict['inputs'] = dict()
        for input in self.inputs:
            # Solve source output index for Links:
            if input.is_link:
                # Skip invalid links:
                if input.value.source_node_id == None:
                    continue
                source_node = next(iter([node for node in all_nodes if node.id == input.value.source_node_id]), None)
                if not source_node:
                    raise Exception(f"Failed to convert Workflow to API Prompt. Node \"{self.title}\" (#{self.id})'s input \"{input.name}\" ({input.type}) is linked to an unknown node ID ({input.value.source_node_id}).")
                api_dict['inputs'][input.name] = [
                    input.value.source_node_id, 
                    source_node.get_output_index_by_name(input.value.source_node_output_name)]
            else:
                api_dict['inputs'][input.name] = input.value
        return api_dict
    