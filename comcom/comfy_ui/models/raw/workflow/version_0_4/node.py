from typing import Union, Optional, List, Dict, Tuple
from pydantic import BaseModel, ConfigDict, Field, AliasPath

from .link_input import Comfy_V0_4_LinkInput
from .output import Comfy_V0_4_Output

from comcom.comfy_ui.models.normalized.workflow.node import NormalizedNode
from comcom.comfy_ui.models.normalized.node_definition.node_definition import NormalizedNodeDefinition

class Comfy_V0_4_Node(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)
    id: str
    title: Optional[str | None] = None
    type: str
    mode: int
    link_inputs: list[Comfy_V0_4_LinkInput] = Field(validation_alias=AliasPath('inputs'), default=[])
    outputs: list[Comfy_V0_4_Output]
    widgets_values: Optional[list[Union[int, str, None]]] = []

    @property
    def muted(self) -> bool:
        return self.mode == 4
    
    def to_normalized(self, node_definitions: List[NormalizedNodeDefinition]) -> NormalizedNode:
        return NormalizedNode(
            id=self.id,
            title=self.title,
            type=self.type,
            mode=self.mode,
            link_inputs=[link_input.to_normalized() for link_input in self.link_inputs],
            outputs=[output.to_normalized() for output in self.outputs],
            widgets_values=self.widgets_values,
            node_definitions=node_definitions
        )

    def get_link_input(self, input_name: str) -> Comfy_V0_4_LinkInput | None:
        for link_input in self.link_inputs:
            if link_input.name == input_name:
                return link_input
        return None
    
    def get_output(self, output_name: str) -> Comfy_V0_4_Output | None:
        for output in self.outputs:
            if output.name == output_name:
                return output
        return None