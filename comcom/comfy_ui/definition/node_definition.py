
from typing import Dict, List, Self
from pydantic import BaseModel, Field, AliasPath

from .input_definitions import InputDefinitions
from comcom.comfy_ui.definition.input_definition import InputDefinition

from comcom.comfy_ui.abstract.abstract_io_definition import AbstractIODefinition

class NodeDefinition(BaseModel, AbstractIODefinition):
    input_definitions: InputDefinitions = Field(validation_alias=AliasPath('input'))

    # TODO This field needs to be aliased, and the real `input_order` should be a @property that scans `input` for virtual inputs.
    # let's wait until we know we actually need `input_order` though - it might be unecessary.
    # I'm disabling it for now so I dont accidentally use it, provided the data is wrong.
    #input_order: Dict[str, List[str]]

    output: List[str]
    output_name: List[str]
    name: str
    display_name: str
    output_node: bool

    @property
    def inputs(self) -> Dict[str, InputDefinition]:
        return self.input_definitions.all
    
    @property
    def outputs(self):
        # TODO: Figure out what to do with this.
        raise Exception("Why was this called?")