from dataclasses import dataclass

from comcom.comfy_ui.models.common.input import Input
from comcom.comfy_ui.models.common.link import Link
from comcom.comfy_ui.models.normalized.node_definition.slot_definition import NormalizedSlotDefinition
@dataclass
class NormalizedInput:
    name: str
    type: str
    value: int | float | str | bool | None
    is_link: bool

    def to_common(self, nodes: list) -> Input:
        # resolve self and then convert into a CommonInput
        def find_source_node_id_and_output_name_and_slot(nodes) -> tuple[str, str, int]:
            for node in nodes:
                for i in range(len(node.outputs)):
                    if self.value in node.outputs[i].links:
                        return node.id, node.outputs[i].name, i
            return None, None, None

        if self.is_link:
            source_node_id, source_node_output_name, source_node_output_index = find_source_node_id_and_output_name_and_slot(nodes)
            return Input(
                name=self.name,
                type=self.type,
                value=Link(
                    source_node_id=source_node_id,
                    source_node_output_name=source_node_output_name
                )
            )
        
        return Input(
            name=self.name,
            type=self.type,
            value=self.value
        )
    
    def apply_prefix_to_link(self, prefix):
        if self.is_link and self.value != None:
            self.value = "{}:{}".format(prefix, self.value)

    def to_slot_definition(self):
        return NormalizedSlotDefinition(
            name=self.name,
            type=self.type,
            metadata={}
        )