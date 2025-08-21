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
        # outputs: List[str]
        # output_name: List[str]
