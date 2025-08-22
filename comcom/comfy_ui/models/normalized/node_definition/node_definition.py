from typing import List
from .slot_definition import NormalizedSlotDefinition

class NormalizedNodeDefinition:
    name: str
    display_name: str
    output_node: bool
    input_slot_definitions: List[NormalizedSlotDefinition]
    output_slot_definitions: List[NormalizedSlotDefinition]

    def __init__(
            self, 
            name: str,
            display_name: str,
            output_node: bool,
            input_slot_definitions: List[NormalizedSlotDefinition],
            output_slot_definitions: List[NormalizedSlotDefinition]):
        
        self.name = name
        self.display_name = display_name
        self.output_node = output_node
        self.input_slot_definitions = input_slot_definitions
        self.output_slot_definitions = output_slot_definitions

    def get_input_slot_definition(self, name: str) -> NormalizedSlotDefinition | None:
        return next((slot for slot in self.input_slot_definitions if slot.name == name), None)

    def get_output_slot_definition(self, name: str) -> NormalizedSlotDefinition | None:
        return next((slot for slot in self.output_slot_definitions if slot.name == name), None)