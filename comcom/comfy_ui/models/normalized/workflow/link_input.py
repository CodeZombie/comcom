from dataclasses import dataclass

from comcom.comfy_ui.models.normalized.node_definition.slot_definition import NormalizedSlotDefinition

@dataclass
class NormalizedLinkInput:
    name: str
    type: str
    widget_name: str | None
    link: str | None

    source_node_id: str | None = None
    source_node_output_index: int | None = None

    @property
    def is_resolved(self):
        return self.source_node_id != None and self.source_node_output_index != None
    
    def apply_prefix_to_link(self, prefix):
        if self.link != None:
            self.link = "{}:{}".format(prefix, self.link)


    def to_slot_definition(self):
        return NormalizedSlotDefinition(
            name=self.name,
            type=self.type,
            metadata={'widget_name': self.widget_name} if self.widget_name != None else {}
        )