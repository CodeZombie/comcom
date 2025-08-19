from typing import List

from comcom.comfy_ui.workflow_graph.node import ComfyNode

class ApiInput:
    def __init__(self):
        self.link_id = None
        self.value: int | str | List[str, int] | None
    
    @property
    def is_link(self):
        return self.link_id != None
    
    def resolve_link(self, nodes: List[ComfyNode]):
        pass