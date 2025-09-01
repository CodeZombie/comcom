from typing import Dict, Any, List, Optional
from pydantic import BaseModel, field_validator

from .input_definition import Comfy_v1_0_InputDefinition

from comcom.comfy_ui.models.normalized.node_definition.slot_definition import NormalizedSlotDefinition

class _VirtualInputDefinitionInsertionRule:
    def __init__(self, match_name: str | None, match_type: str | None, match_metadata: dict[str, Any] | None, new_input_name: str, new_input_type: str):
        self.match_name = match_name
        self.match_type = match_type
        self.match_metadata = match_metadata
        self.new_input_name = new_input_name
        self.new_input_type = new_input_type
    
    def create_input_if_match(self, input: Comfy_v1_0_InputDefinition, input_name: str) -> Dict[str, Comfy_v1_0_InputDefinition]:
        if self.match_name != None:
            if self.match_name != input_name:
                return {}
        
        if self.match_type != None:
            if self.match_type != input.type:
                return {}
        
        if self.match_metadata != None:
            for match_metadata_key, match_metadata_value in self.match_metadata.items():
                if input.metadata.get(match_metadata_key) != match_metadata_value:
                    return {}
        return {self.new_input_name: Comfy_v1_0_InputDefinition([self.new_input_type, {}])}
        
# HACK: ComfyUI hardcodes a virtual input called 'control_after_generate' to come after all ('seed', INT) and ('noise_seed', INT) inputs.
# We have to detect this to make sure all the widget_values align with their input names.
# https://github.com/Comfy-Org/ComfyUI_frontend/blob/daf94d74d53739e65920dd2966aca77777fd7c53/src/scripts/widgets.ts#L384-L386
VIRTUAL_INPUT_DEFINITION_INSERTION_RULES = [
    _VirtualInputDefinitionInsertionRule(match_name='seed', match_type='INT', match_metadata=None, new_input_name='control_after_generate', new_input_type='STRING'),
    _VirtualInputDefinitionInsertionRule(match_name='noise_seed', match_type='INT', match_metadata=None, new_input_name='control_after_generate', new_input_type='STRING'),
    _VirtualInputDefinitionInsertionRule(match_name=None, match_type='INT', match_metadata={'control_after_generate': True}, new_input_name='control_after_generate', new_input_type='STRING')
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
                output.update(virtual_input_insertion_rule.create_input_if_match(output[key], key))
        return output
        
    @property
    def all(self) -> Dict[str, Comfy_v1_0_InputDefinition]:
        return self.required | self.optional
    
    def to_normalized(self) -> Dict[str, Comfy_v1_0_InputDefinition]:
        return [NormalizedSlotDefinition(name=input_name, type=input_def.type, metadata=input_def.metadata) for input_name, input_def in self.all.items()]
    