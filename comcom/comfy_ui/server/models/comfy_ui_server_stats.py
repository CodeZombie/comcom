from typing import Dict
from pydantic import BaseModel, Field, AliasPath, field_validator

class ComfyUIServerStatsRequest:
    endpoint: str = "system_stats"

class ComfyUIServerStatsResponse(BaseModel):
    version_str: str = Field(validation_alias=AliasPath('system', 'comfyui_version'), default=None)
    version: Dict[str, int] = Field(validation_alias=AliasPath('system', 'comfyui_version'), default=None)
    python_version: str = Field(validation_alias=AliasPath('system', 'python_version'), default=None)

    @field_validator('version', mode='before')
    @classmethod
    def convert_semantic_version_from_str_to_dict(cls, version_str: str) -> Dict[str, int]:
        semantic_version_labels = ['major', 'minor', 'patch']
        return dict(zip(semantic_version_labels, [int(x) for x in version_str.split('.')] ))
    
    # @property
    # def endpoint(self) -> str:
    #     return "system_stats"
