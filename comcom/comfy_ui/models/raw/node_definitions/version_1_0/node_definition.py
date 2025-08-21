# pylint: disable=no-member

from typing import Dict, List, Self
from pydantic import BaseModel, Field, AliasPath

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