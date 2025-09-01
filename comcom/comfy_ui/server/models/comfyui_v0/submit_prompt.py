from dataclasses import dataclass
import json
from typing import Dict, List, Optional
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

class ComfyUI_v0_SubmitPromptErrorResponseModel_Error(BaseModel):
    type: str
    message: str
    details: str
    extra_info: Optional[Dict]

    def __str__(self):
        if self.details:
            return f"{self.details}: {self.message} ({self.type})"
        return f"{self.message} ({self.type})"

class ComfyUI_v0_SubmitPromptErrorResponseModel_NodeErrors(BaseModel):
    errors: List[ComfyUI_v0_SubmitPromptErrorResponseModel_Error]
    dependent_outputs: Optional[List[str | int]] = []
    class_type: Optional[str] = ""

    def __str__(self):
        r = f"({self.class_type}):\n"
        for error in self.errors:
            r += f"    - {str(error)}\n"
        return r

@dataclass
class ComfyUI_v0_SubmitPromptErrorResponseModel(BaseModel):
    error: ComfyUI_v0_SubmitPromptErrorResponseModel_Error
    node_errors: Dict[str, ComfyUI_v0_SubmitPromptErrorResponseModel_NodeErrors]

    def __str__(self):
        r = f"{str(self.error)}\n"
        for node_id, node_error in self.node_errors.items():
            r += f"Node #{node_id}: {str(node_error)}\n"
        return r