from typing import Dict, Self

from comcom.comfy_ui.definition.node_definitions import NodeDefinitions
from comcom.comfy_ui.workflow_graph.node import ComfyNode

from .input import ApiInput

class ApiNode:
    def __init__(self, class_type: str, inputs: Dict[str, ApiInput] = {}):
        self.class_type: str = class_type
        self.inputs: Dict[str, ApiInput] = inputs

    @classmethod
    def from_comfy_node(cls, comfy_node: ComfyNode, node_definitions: NodeDefinitions) -> Self:
        pass