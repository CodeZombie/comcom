from typing import Dict, Any, List, Optional
from pydantic import BaseModel, field_validator

from .input_definition import Comfy_v1_0_InputDefinition

from comcom.comfy_ui.models.normalized.node_definition.slot_definition import NormalizedSlotDefinition

class _VirtualInputDefinitionInsertionRule:
    def __init__(self, match_type: str, match_metadata: dict[str, Any], new_input_name: str, new_input_type: str):
        self.match_type = match_type
        self.match_metadata = match_metadata
        self.new_input_name = new_input_name
        self.new_input_type = new_input_type
    
    def create_input_if_match(self, input: Comfy_v1_0_InputDefinition) -> Dict[str, Comfy_v1_0_InputDefinition]:
        new_input_definitions: Dict[str, Comfy_v1_0_InputDefinition] = {}
        if input.type == self.match_type:
            for metadata_key in self.match_metadata.keys():
                if metadata_key in input.metadata.keys() and input.metadata.get(metadata_key) == self.match_metadata.get(metadata_key):
                    new_input_definitions[self.new_input_name] = Comfy_v1_0_InputDefinition(['INT', {}])
        return new_input_definitions
        

VIRTUAL_INPUT_DEFINITION_INSERTION_RULES = [
    _VirtualInputDefinitionInsertionRule(match_type='INT', match_metadata={'control_after_generate': True}, new_input_name='control_after_generate', new_input_type='STRING')
]

class Comfy_v1_0_InputDefinitions(BaseModel):
    required: Optional[Dict[str, Comfy_v1_0_InputDefinition]] = {}
    optional: Optional[Dict[str, Comfy_v1_0_InputDefinition]] = {}

    @field_validator('required', 'optional', mode='before')
    @classmethod
    def insert_virtual_inputs(cls, input_defs_dict: Dict[str, List[str | List | Dict[str, Any] | None]]) -> Dict[str, Comfy_v1_0_InputDefinition]:
        output: Dict[str, Comfy_v1_0_InputDefinition] = {}
        for key in input_defs_dict.keys():
            output[key] = Comfy_v1_0_InputDefinition(input_defs_dict[key])
            for virtual_input_insertion_rule in VIRTUAL_INPUT_DEFINITION_INSERTION_RULES:
                output.update(virtual_input_insertion_rule.create_input_if_match(output[key]))
        return output
        
    @property
    def all(self) -> Dict[str, Comfy_v1_0_InputDefinition]:
        return self.required | self.optional
    
    def to_normalized(self) -> Dict[str, Comfy_v1_0_InputDefinition]:
        return [NormalizedSlotDefinition(name=input_name, type=input_def.type, metadata=input_def.metadata) for input_name, input_def in self.all.items()]
    