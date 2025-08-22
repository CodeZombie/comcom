from dataclasses import dataclass
from typing import Any

@dataclass
class Bypass:
    source_link_id: str # This will be an Output link id
    input_link_id_that_needs_to_be_changed: str # this will be an input link id. This is the the id that will get changed.
    is_raw_value: bool = False
    raw_value: Any = None