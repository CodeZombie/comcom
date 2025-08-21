from typing import List, Dict
from dataclasses import dataclass

import copy

from comcom.comfy_ui.models.normalized.abstract.abstract_io_definition import AbstractIODefinition

from .input import NormalizedInput
from .link_input import NormalizedLinkInput
from .output import NormalizedOutput

@dataclass
class NormalizedNode:
    id: str
    type: str
    mode: int
    link_inputs: List[NormalizedLinkInput] 
    outputs: List[NormalizedOutput]
    widgets_values: List[int | str | None]

    @property
    def muted(self) -> bool:
        return self.mode == 4

    # TODO: Refactor NodeDefinition and SubgraphDefinition so they both implement equiavlent `inputs` and `outputs` getters that return the exact same type (idealy dicts)
    def get_inputs(self, node_definition: AbstractIODefinition) -> Dict[str, NormalizedInput]:

        # Go through a list of every input.
        input_names = list(node_definition.inputs.keys())

        #input_names_with_widgets = [link_input.name for link_input in self.link_inputs]
        link_inputs: Dict[str, NormalizedInput] = dict()
        for link_input in self.link_inputs:
            link_inputs[link_input.name] = NormalizedInput(
                name=link_input.name, 
                type=link_input.type, 
                value=link_input.link,
                is_link=True)
            
            if not link_input.widget_name:
                input_names.remove(link_input.name)

        # `input_names` should now map directly to `widget_values`
        value_inputs: Dict[str, NormalizedInput] = dict()
        for i in range(len(input_names)):
            input_name: str = input_names[i]
            input_definition = node_definition.inputs[input_name]
            value_inputs[input_name] = NormalizedInput(
                name=input_name,
                type=input_definition.type,
                value=self.widgets_values[i],
                is_link=False
            )

        return value_inputs | link_inputs
    
    def get_bypass_map(self, node_definition: AbstractIODefinition):
        class Found(Exception): pass
        bypass_map: dict[str, str] = {}
        inputs: list[NormalizedInput] = self.get_inputs(node_definition)

        for output in self.outputs:
            for inp in inputs:
                try:
                    if inp.type == output.type:
                        for link_id in output.link_ids:
                            source_link_id = inp.value.id if inp.is_link else None
                            if source_link_id != None:
                                if source_link_id not in bypass_map.keys():
                                    bypass_map[source_link_id] = []
                                bypass_map[source_link_id].append(link_id)
                        inputs.remove(inp)
                        raise Found
                except Found:
                    break

        return bypass_map