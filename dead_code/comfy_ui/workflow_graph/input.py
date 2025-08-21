from typing import List
from dataclasses import dataclass

from comfy_ui.abstract.abstract_slot import AbstractSlot

@dataclass(frozen=True)
class ComfyInput(AbstractSlot):
    name: str
    type: str
    value: int | str | List | None
    is_link: bool

    