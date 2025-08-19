from pydantic import BaseModel

from .node import ComfyNode
from .output import ComfyOutput

class AbstractGraph(BaseModel):
    id: str
    revision: int
    nodes: list[ComfyNode]
    version: float

    def get_node(self, id: str):
        for node in self.nodes:
            if node.id == id:
                return node
        return None
    
    def get_link_source(self, link_id: str) -> tuple[ComfyNode, ComfyOutput] | None:
        for node in self.nodes:
            for output in node.outputs:
                if link_id in output.links:
                    return tuple(node, output)
        return None