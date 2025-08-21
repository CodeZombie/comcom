from typing import List, Optional

from pydantic import BaseModel, ConfigDict, field_validator

class ComfyOutput(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)

    name: str
    type: str
    links: list[str]

    @field_validator('links', mode='before')
    @classmethod
    def none_to_empty_list(cls, v: Optional[List[str]]) -> List[str]:
        if v is None:
            return []
        return v