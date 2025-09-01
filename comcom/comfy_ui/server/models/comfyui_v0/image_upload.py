from typing import Any
from dataclasses import dataclass
from pydantic import BaseModel

from comcom.comfy_ui.file_management.remote_file import RemoteFile

@dataclass
class ComfyUI_v0_ImageUploadRequestModel:
    filename: str
    image_data: Any
    subfolder: str = ""
    overwrite: bool = True
    type: str = "input"

    @property
    def data(self):
        return {
            'overwrite': "true" if self.overwrite else "false", # Yuck! https://github.com/comfyanonymous/ComfyUI/blob/b1fd26fe9e55163f780bf9e5f56bf9bf5f035c93/server.py#L181
            'type': self.type,
            "subfolder": self.subfolder}
    
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
    name: str
    subfolder: str
    type: str

    def to_remote_file(self):
        return RemoteFile(
            filename=self.name,
            type=self.type,
            subfolder=self.subfolder
        )

# The `upload/image` endpoint doesn't seem to actually return a useful json error message.
# It doesn't seem to care if the image data is malformed, or if `type` is a non-bool.
# If it really gets into trouble (filename = "", or type = "FAKE"), it'll just HTTP 500.
# So I think this class doesn't have a purpose (yet)
class ComfyUI_v0_ImageUploadErrorResponseModel(BaseModel):
    pass