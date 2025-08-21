from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, AliasPath

class ComfyLinkInput(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)
    
    name: str
    type: str
    widget_name: Optional[str | None] = Field(validation_alias=AliasPath('widget', 'name'), default=None)
    link: str | None