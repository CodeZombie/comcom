from dataclasses import dataclass

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