from dataclasses import dataclass

from comcom.comfy_ui.models.normalized.node_definition.slot_definition import NormalizedSlotDefinition

@dataclass
class NormalizedOutput:
    name: str
    type: str
    links: list[str]

    def apply_prefix_to_links(self, prefix):
        new_links: list[str] = []
        for link_id in self.links:
            if link_id != None:
                new_links.append("{}:{}".format(prefix, link_id))
        self.links = new_links

    def to_slot_definition(self):
        return NormalizedSlotDefinition(
            name=self.name,
            type=self.type,
            metadata={}
        )