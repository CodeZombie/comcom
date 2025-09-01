from dataclasses import dataclass
import json
from typing import Dict, List
from pydantic import BaseModel, RootModel

from comcom.comfy_ui.file_management.remote_file import RemoteFile

@dataclass
class ComfyUI_v0_SubmitPromptRequestModel:
    prompt_api_dict: Dict
    client_id: str

    @property
    def endpoint(self):
        return f"prompt"

    @property
    def data(self):
        return {
            'prompt': self.prompt_api_dict,
            'client_id': self.client_id
        }
    
    @property
    def data_json(self):
        return json.dumps(self.data).encode('utf-8')
    
@dataclass
class ComfyUI_v0_SubmitPromptResponseModel(BaseModel):
    pass

@dataclass
class ComfyUI_v0_SubmitPromptErrorResponseModel(BaseModel):
    pass

