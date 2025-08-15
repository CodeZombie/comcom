from dataclasses import dataclass
#from typing import Union

@dataclass
class APILink:
    source_node_id: str
    output_id: int

@dataclass
class APINode:
    id: str
    #inputs: dict[str, Union[int, float, str, bool, APILink]]

@dataclass
class APIPrompt:
    nodes: list[APINode]