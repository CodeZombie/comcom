from typing import List, Optional

from pydantic import BaseModel, ConfigDict, field_validator, Field, AliasChoices

from comcom.comfy_ui.models.normalized.workflow.output import NormalizedOutput

class Comfy_V0_4_Output(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)

    name: str
    type: str
    links: list[str] = Field(validation_alias=AliasChoices('links', 'linkIds'), default=[])

    @field_validator('links', mode='before')
    @classmethod
    def none_to_empty_list(cls, v: Optional[List[str]]) -> List[str]:
        if v is None:
            return []
        return v

    def to_normalized(self) -> NormalizedOutput:
        return NormalizedOutput(
            name=self.name,
            type=self.type,
            links=self.links,
        )

    