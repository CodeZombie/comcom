from typing import Union, Optional, List, Dict, Tuple
from pydantic import BaseModel, ConfigDict, Field, AliasPath

from .link_input import ComfyLinkInput
from .output import ComfyOutput

from comcom.comfy_ui.definition.node_definition import NodeDefinition
from comcom.comfy_ui.workflow_graph.input import ComfyInput

from comcom.comfy_ui.abstract.abstract_io_definition import AbstractIODefinition

class ComfyNode(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)
    id: str
    type: str
    mode: int
    link_inputs: list[ComfyLinkInput] = Field(validation_alias=AliasPath('inputs'), default=[])
    outputs: list[ComfyOutput]
    widgets_values: Optional[list[Union[int, str, None]]] = []

    @property
    def muted(self) -> bool:
        return self.mode == 4
    
    def get_output_location_from_link(self, link_id: str) -> Tuple[str | None, int | None]:
        for i in range(len(self.outputs)):
            if link_id in self.outputs[i].links:
                return (self.id, i)
        return None

    def get_link_input(self, input_name: str) -> ComfyLinkInput | None:
        for link_input in self.link_inputs:
            if link_input.name == input_name:
                return link_input
        return None
    
    def get_input(self, input_name: str, node_definition: NodeDefinition) -> ComfyInput | None:
        comfy_inputs: Dict[str, ComfyInput] = self.get_inputs(node_definition)
        return comfy_inputs.get(input_name, None)
    
    def get_outputs(self) -> list[ComfyOutput]:
        return self.outputs

    # TODO: Refactor NodeDefinition and SubgraphDefinition so they both implement equiavlent `inputs` and `outputs` getters that return the exact same type (idealy dicts)
    def get_inputs(self, node_definition: AbstractIODefinition) -> Dict[str, ComfyInput]:

        # Go through a list of every input.
        input_names = list(node_definition.inputs.keys())

        #input_names_with_widgets = [link_input.name for link_input in self.link_inputs]
        link_inputs: Dict[str, ComfyInput] = dict()
        for link_input in self.link_inputs:
            link_inputs[link_input.name] = ComfyInput(
                name=link_input.name, 
                type=link_input.type, 
                value=link_input.link,
                is_link=True)
            
            if not link_input.widget_name:
                input_names.remove(link_input.name)

        # `input_names` should now map directly to `widget_values`
        value_inputs: Dict[str, ComfyInput] = dict()
        for i in range(len(input_names)):
            input_name: str = input_names[i]
            input_definition = node_definition.inputs[input_name]
            value_inputs[input_name] = ComfyInput(
                name=input_name,
                type=input_definition.type,
                value=self.widgets_values[i],
                is_link=False
            )

        return value_inputs | link_inputs
    