from dataclasses import dataclass
from typing import Dict, List, Optional
from pydantic import BaseModel, RootModel

from comcom.comfy_ui.file_management.remote_file import RemoteFile

@dataclass
class ComfyUI_v0_PromptHistoryRequestModel:
    prompt_id: str

    @property
    def endpoint(self):
        return f"history/{self.prompt_id}"
    

class ComfyUI_v0_PromptHistoryResponseModel_ImageOutput(BaseModel):
    filename: str
    subfolder: str
    type: str

    def to_remote_file(self):
        return RemoteFile(
            filename=self.filename,
            type=self.type,
            subfolder=self.subfolder,
        )

# class ComfyUI_v0_PromptHistoryResponseModel_OutputCategory(BaseModel):
#     images: Optional[List[ComfyUI_v0_PromptHistoryResponseModel_ImageOutput]] = []
    
class ComfyUI_v0_PromptHistoryResponseModel_Node(BaseModel):
    images: Optional[List[ComfyUI_v0_PromptHistoryResponseModel_ImageOutput]] = []

class ComfyUI_v0_PromptHistoryResponseModel_Prompt(BaseModel):
    outputs: Optional[Dict[str, ComfyUI_v0_PromptHistoryResponseModel_Node]] = {}

class ComfyUI_v0_PromptHistoryResponseModel(RootModel[Dict[str,  ComfyUI_v0_PromptHistoryResponseModel_Prompt]]):

    def get_output_nodes_from_prompt_id(self, prompt_id: str) -> Dict[str, ComfyUI_v0_PromptHistoryResponseModel_Node]:
        prompt_history = self.root.get(prompt_id, None)
        if prompt_history:
            return prompt_history.outputs

        return {}