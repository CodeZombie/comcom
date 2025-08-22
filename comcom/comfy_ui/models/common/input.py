from dataclasses import dataclass

from .link import Link

@dataclass
class Input:
    name: str
    type: str
    value: int | float | str | bool | Link | None

    @property
    def is_link(self):
        return isinstance(self.value, Link)
