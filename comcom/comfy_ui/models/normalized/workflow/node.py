from typing import List, Dict
from dataclasses import dataclass

from comcom.comfy_ui.exceptions import WorkflowParseError

from comcom.comfy_ui.models.normalized.abstract.abstract_io_definition import AbstractIODefinition
from comcom.comfy_ui.models.normalized.node_definition.node_definition import NormalizedNodeDefinition
from comcom.comfy_ui.models.normalized.node_definition.slot_definition import NormalizedSlotDefinition

from comcom.comfy_ui.models.normalized.utils.bypass import Bypass


from .input import NormalizedInput
from .link_input import NormalizedLinkInput
from .output import NormalizedOutput

class NormalizedNode:
    id: str
    type: str
    mode: int
    inputs: List[NormalizedInput]
    outputs: List[NormalizedOutput]

    def __init__(
            self, 
            id: str, 
            type: str, 
            mode: int, 
            link_inputs: List[NormalizedLinkInput], 
            widgets_values: List[int | str | None], 
            outputs: List[NormalizedOutput], 
            node_definitions: List[NormalizedNodeDefinition]):
        
        self.id = id
        self.type = type
        self.mode = mode
        self.outputs = outputs

        reroute_definition: NormalizedNodeDefinition = NormalizedNodeDefinition(
            name="Reroute",
            display_name="Reroute",
            output_node=True,
            input_slot_definitions=[NormalizedSlotDefinition(name="", type="*", metadata={})],
            output_slot_definitions=[NormalizedSlotDefinition(name="", type="*", metadata={})],
        )

        # Resolve inputs
        node_definitions = [reroute_definition] + node_definitions
        node_definition: NormalizedNodeDefinition = next((node_definition for node_definition in node_definitions if node_definition.name == type), None)
        if not node_definition:
            raise WorkflowParseError("Node Definition {} does not exist.".format(self.type))

        input_names = [input_slot.name for input_slot in node_definition.input_slot_definitions]

        #input_names_with_widgets = [link_input.name for link_input in self.link_inputs]
        new_link_inputs: Dict[str, NormalizedInput] = dict()
        for link_input in link_inputs:
            new_link_inputs[link_input.name] = NormalizedInput(
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
            input_definition = node_definition.get_input_slot_definition(input_name)
            value_inputs[input_name] = NormalizedInput(
                name=input_name,
                type=input_definition.type,
                value=widgets_values[i] if len(widgets_values) > i else None,
                is_link=False
            )

        self.inputs = list((value_inputs | new_link_inputs).values())

    @property
    def muted(self) -> bool:
        return self.mode == 4

    def apply_prefix_to_links(self, prefix):
        for input in self.inputs:
            if input.is_link:
                input.value = "{}:{}".format(prefix, input.value)
        for output in self.outputs:
            new_link_ids = []
            for link_id in output.links:
                new_link_ids.append("{}:{}".format(prefix, link_id))
            output.links = new_link_ids
    
    def get_bypasses(self) -> List[Bypass]:
        class Found(Exception): pass
        bypasses: List[Bypass] = []
        inputs: list[NormalizedInput] = self.inputs.copy()

        for output in self.outputs:
            for inp in inputs:
                try:
                    if inp.type == output.type or inp.type == "*":
                        for link_id in output.links:
                            source_link_id = inp.value if inp.is_link else None
                            if source_link_id != None:
                                bypasses.append(Bypass(source_link_id=source_link_id, input_link_id_that_needs_to_be_changed=link_id))
                        inputs.remove(inp)
                        raise Found
                except Found:
                    break
        return bypasses
    

    def apply_bypasses(self, bypasses: List[Bypass]):
        for bypass in bypasses:
            self.apply_bypass(bypass)

    def apply_bypass(self, bypass: Bypass):
        for input in self.inputs:
            if input.is_link:
                if input.value == bypass.input_link_id_that_needs_to_be_changed:
                    input.value = bypass.raw_value if bypass.is_raw_value else bypass.source_link_id
                    if bypass.is_raw_value:
                        input.is_link = False
                    