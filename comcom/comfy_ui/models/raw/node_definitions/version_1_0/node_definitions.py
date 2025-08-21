from typing import Dict, List, Any
from pydantic import RootModel, model_validator

from .node_definition import Comfy_v1_0_NodeDefinition

from comcom.comfy_ui.models.normalized.node_definition.node_definition import NormalizedNodeDefinition

class Comfy_v1_0_NodeDefinitions(RootModel[List[Comfy_v1_0_NodeDefinition]]):

    @model_validator(mode='before')
    @classmethod
    def parse_input(cls, values: Dict[str, Dict[str, Any]]) -> List[Comfy_v1_0_NodeDefinition]:
        if not isinstance(values, Dict):
            raise ValueError('Input must be a dict')
        
        validated_node_definitions: List[Comfy_v1_0_NodeDefinition] = []

        for node_definition_name, node_definition_dict in values.items():
            node_definition_dict['name'] = node_definition_name
            validated_node_definitions.append(Comfy_v1_0_NodeDefinition(**node_definition_dict))

        return validated_node_definitions

    def get_node_definition(self, type_name: str) -> Comfy_v1_0_NodeDefinition | None:
        for node_definition in self.root:
            if node_definition.name == type_name:
                return node_definition
        return None
    
    def to_normalized(self) -> List[NormalizedNodeDefinition]:
        return [node_definition.to_normalized() for node_definition in self.root]

