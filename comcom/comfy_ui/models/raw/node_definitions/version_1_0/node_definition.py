# pylint: disable=no-member

from typing import Dict, List, Self, Any
from pydantic import BaseModel, Field, AliasPath, field_validator

from .input_definitions import Comfy_v1_0_InputDefinitions

from comcom.comfy_ui.models.normalized.node_definition.node_definition import NormalizedNodeDefinition

class Comfy_v1_0_NodeDefinition(BaseModel):
    name: str
    display_name: str
    output_node: bool
    input_definitions: Comfy_v1_0_InputDefinitions = Field(validation_alias=AliasPath('input'))
    output: List[str]
    output_name: List[str]

    # TODO This field needs to be aliased, and the real `input_order` should be a @property that scans `input` for virtual inputs.
    # let's wait until we know we actually need `input_order` though - it might be unecessary.
    # I'm disabling it for now so I dont accidentally use it, given the data will be wrong in some cases.
    #input_order: Dict[str, List[str]]


    # A Node Definition's `output` (Which is supposed to list the Types of each output) will sometimes contains 
    # a List of strings (ie ImpactSchedulerAdapter). I think it being a list (of all possible outputs, I think?) it indicates that
    # This node's output is `LIST`. I'm not sure though, and I really can't think of a trivial way to confirm.
    # I'm rolling with this theory for now.
    @field_validator('output', mode='before')
    def _sanitize_output(cls, values: Any) -> List[str]:
        results: List[str] = []
        for item in values:
            if isinstance(item, list):
                results.append("LIST")
            else:
                results.append(item)
        return results


    @property
    def inputs(self) -> Dict[str, Comfy_v1_0_InputDefinitions]:
        return self.input_definitions.all
    
    @property
    def outputs(self):
        # TODO: Figure out what to do with this.
        raise Exception("Why was this called?")
    
    def to_normalized(self) -> Self:
        return NormalizedNodeDefinition(
            name=self.name,
            display_name=self.display_name,
            input_slot_definitions=self.input_definitions.to_normalized(),
            output_slot_definitions=[],
            output_node=self.output_node
        )