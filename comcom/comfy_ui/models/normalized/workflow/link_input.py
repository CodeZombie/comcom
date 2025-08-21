from dataclasses import dataclass
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
    
