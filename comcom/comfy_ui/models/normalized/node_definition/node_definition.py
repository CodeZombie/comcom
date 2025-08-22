from typing import List
from dataclasses import dataclass
from .slot_definition import NormalizedSlotDefinition

@dataclass
class NormalizedNodeDefinition:
    name: str
    display_name: str
    output_node: bool
    input_slot_definitions: List[NormalizedSlotDefinition]
    output_slot_definitions: List[NormalizedSlotDefinition]
    is_subgraph: bool = False

    def get_input_slot_definition(self, name: str) -> NormalizedSlotDefinition | None:
        return next((slot for slot in self.input_slot_definitions if slot.name == name), None)

    def get_output_slot_definition(self, name: str) -> NormalizedSlotDefinition | None:
        return next((slot for slot in self.output_slot_definitions if slot.name == name), None)