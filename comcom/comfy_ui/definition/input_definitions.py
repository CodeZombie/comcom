from typing import Dict, Any, List
from typing_extensions import Optional
from pydantic import BaseModel, field_validator

from .input_definition import InputDefinition

class _VirtualInputDefinitionInsertionRule:
    def __init__(self, match_type: str, match_metadata: dict[str, Any], new_input_name: str, new_input_type: str):
        self.match_type = match_type
        self.match_metadata = match_metadata
        self.new_input_name = new_input_name
        self.new_input_type = new_input_type
    
    def create_input_if_match(self, input: InputDefinition) -> Dict[str, InputDefinition]:
        new_input_definitions: Dict[str, InputDefinition] = {}
        if input.type == self.match_type:
            for metadata_key in self.match_metadata.keys():
                if metadata_key in input.metadata.keys() and input.metadata.get(metadata_key) == self.match_metadata.get(metadata_key):
                    new_input_definitions[self.new_input_name] = InputDefinition(['INT', {}])
        return new_input_definitions
        

VIRTUAL_INPUT_DEFINITION_INSERTION_RULES = [
    _VirtualInputDefinitionInsertionRule(match_type='INT', match_metadata={'control_after_generate': True}, new_input_name='control_after_generate', new_input_type='STRING')
]

class InputDefinitions(BaseModel):
    required: Optional[Dict[str, InputDefinition]] = {}
    optional: Optional[Dict[str, InputDefinition]] = {}

    @field_validator('required', 'optional', mode='before')
    @classmethod
    def insert_virtual_inputs(cls, input_defs_dict: Dict[str, List[str | List | Dict[str, Any] | None]]) -> Dict[str, InputDefinition]:
        output: Dict[str, InputDefinition] = {}
        for key in input_defs_dict.keys():
            output[key] = InputDefinition(input_defs_dict[key])
            for virtual_input_insertion_rule in VIRTUAL_INPUT_DEFINITION_INSERTION_RULES:
                output.update(virtual_input_insertion_rule.create_input_if_match(output[key]))
        return output
        
    @property
    def all(self) -> Dict[str, InputDefinition]:
        return self.required | self.optional