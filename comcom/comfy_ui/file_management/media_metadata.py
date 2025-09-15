from typing import Dict, Any, Self, Optional
from pydantic import BaseModel, field_validator, field_serializer, SerializationInfo
from datetime import datetime
import hashlib
import yaml
import pathlib

from comcom.comfy_ui.file_management.remote_file import RemoteFile
from comcom.comfy_ui.file_management.local_file import LocalFile

class MediaMetadata(BaseModel):
    local_path: Optional[LocalFile] = None
    remote_file: Optional[RemoteFile] = None
    sha1: Optional[str] = None
    upload_time: Optional[datetime] = None

    @field_validator('local_path', mode='before')
    @classmethod
    # TODO: fix this function signature. it's not a local_path_str any more, and i dont think it can ever be type LocalFile
    def _filepath_str_to_localfile(cls, local_path_str: Dict | LocalFile) -> LocalFile | None:
        if isinstance(local_path_str, LocalFile):
            return local_path_str
        return LocalFile(path=local_path_str.get('path'), requires_editing=local_path_str.get('requires_editing', False))

    # @field_serializer('local_path')
    # def _serialize_path(self, lp: LocalFile, info: SerializationInfo) -> str:
    #     return lp.path_str
    
    @property
    def local_file_needs_to_be_edited_but_hasnt_been_edited_yet(self) -> bool:
       """ verbose function names are better than ambiguous ones :) """ 
       if self.local_path.requires_editing and self.sha1 == self.local_path.sha1:
           return True
       return False

    @classmethod
    def from_file(cls, file_path: str) -> Self:
        return cls.model_validate(yaml.load(open(file_path, 'r').read(), Loader=yaml.FullLoader))

    def save(self):
        with open(self.local_path.metadata_path, 'w') as f:
            f.write(yaml.dump(self.model_dump(), default_flow_style=False))

    @property
    def has_sha1(self):
        return self.sha1 != None

    @classmethod
    def from_local_and_remote_files(cls, local_file: LocalFile, remote_file: RemoteFile):
        return cls(
            local_path=local_file,
            remote_file=remote_file,
            sha1=local_file.sha1,
            upload_time=datetime.now()
        )