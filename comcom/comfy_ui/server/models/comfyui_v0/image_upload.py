from typing import Any
from dataclasses import dataclass
from pydantic import BaseModel

@dataclass
class ComfyUI_v0_ImageUploadRequestModel:
    filename: str
    image_data: Any
    subfolder: str = "input"

    @property
    def data(self):
        return {"subfolder": self.subfolder}
    
    @property
    def files(self):
        """
        Despite being called "files" (plural), the ImageUpload endpoint seems to only be able to handle a single image file at a time.
        """
        return {'image': (self.filename, self.image_data)}
    
    @property
    def endpoint(self):
        return "upload/image"

class ComfyUI_v0_ImageUploadResponseModel(BaseModel):
    pass

class ComfyUI_v0_ImageUploadErrorResponseModel(BaseModel):
    pass