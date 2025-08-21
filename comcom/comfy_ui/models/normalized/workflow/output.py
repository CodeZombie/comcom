from dataclasses import dataclass

@dataclass
class NormalizedOutput:
    name: str
    type: str
    links: list[str]