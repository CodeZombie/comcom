from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field, AliasPath, AliasChoices, field_validator
from pydantic_core import PydanticCustomError

from comcom.comfy_ui.models.normalized.workflow.link_input import NormalizedLinkInput


class Comfy_V0_4_LinkInput(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)

    name: str
    type: str
    widget_name: Optional[str | None] = Field(validation_alias=AliasPath('widget', 'name'), default=None)
    link: str | None = Field(validation_alias=AliasChoices('link', 'linkIds'), default=None)

    @field_validator('link', mode='before')
    @classmethod
    def none_to_empty_list(cls, v: Optional[List[str] | str]) -> str | None:
        if isinstance(v, List):
            if len(v) == 1:
                return str(v[0])
            elif len(v) == 0:
                return None
            raise ValueError('Link Input cannot have more than one link')
        if v == None:
            return None
        return str(v)

    def to_normalized(self) -> NormalizedLinkInput:
        return NormalizedLinkInput(
            name=self.name,
            type=self.type,
            widget_name=self.widget_name,
            link=self.link,
        )