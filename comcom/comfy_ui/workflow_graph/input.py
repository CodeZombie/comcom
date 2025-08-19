from typing import List
from dataclasses import dataclass

@dataclass(frozen=True)
class ComfyInput:
    name: str
    type: str
    value: int | str | List | None
    is_link: bool