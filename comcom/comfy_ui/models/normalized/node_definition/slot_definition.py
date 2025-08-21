from dataclasses import dataclass

@dataclass
class NormalizedSlotDefinition:
    name: str
    type: str
    metadata: dict