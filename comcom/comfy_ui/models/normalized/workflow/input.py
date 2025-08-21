from dataclasses import dataclass

from comcom.comfy_ui.models.common.input import Input
from comcom.comfy_ui.models.common.link import Link 

@dataclass
class NormalizedInput:
    name: str
    type: str
    value: int | float | str | bool | None
    is_link: bool

    def to_common(self, nodes: list) -> Input:
        # resolve self and then convert into a CommonInput
        def find_source_node_id_and_output_slot(nodes) -> tuple[str, int]:
            for node in nodes:
                for i in range(len(node.outputs)):
                    if self.value in node.outputs[i].link_ids:
                        return node.id, i
            return None, None

        if self.is_link:
            source_node_id, source_node_output_slot = find_source_node_id_and_output_slot(nodes)
            return Input(
                name=self.name,
                type=self.type,
                value=Link(
                    id=source_node_id,
                    slot=source_node_output_slot
                )
            )
        
        return Input(
            name=self.name,
            type=self.type,
            value=self.value
        )