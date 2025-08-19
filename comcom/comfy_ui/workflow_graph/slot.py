from pydantic import BaseModel, ConfigDict

class ComfySlot(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)
    
    id: str
    name: str
    type: str
    linkIds: list[str]