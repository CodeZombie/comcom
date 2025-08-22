from typing import List
from .node import NormalizedNode
from .link_input import NormalizedLinkInput
from .output import NormalizedOutput

class NormalizedSubgraphNode(NormalizedNode):
    nodes: List[NormalizedNode]
    interior_inputs: List[NormalizedOutput]
    interior_outputs: List[NormalizedLinkInput]


    def __init__(
            self, 
            id: str, 
            type: str, 
            mode: int, 
            link_inputs: List[NormalizedLinkInput], 
            widgets_values: List[int | str | None], 
            outputs: List[NormalizedOutput], 
            node_definitions: List[NormalizedNodeDefinition],
            nodes: List[NormalizedNode],
            interior_inputs: List[NormalizedOutput],
            interior_outputs: List[NormalizedLinkInput]):
        pass