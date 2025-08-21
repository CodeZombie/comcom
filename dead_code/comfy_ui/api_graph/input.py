from typing import List

from comcom.comfy_ui.models.raw.workflow.version_0_4.node import ComfyNode

class ApiInput:
    def __init__(self, link_id: str, source_node_id: str, source_node_output_slot: int):
        self.link_id = None
        self.value: int | str | List[str, int] | None
    
    @property
    def is_link(self):
        return self.link_id != None
    
    def resolve_link(self, nodes: List[ComfyNode]):
        pass