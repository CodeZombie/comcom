from typing import Self, Optional
from pydantic import BaseModel, field_validator, field_serializer, SerializationInfo, Field, AliasPath, AliasChoices
import os
from pathlib import Path
from comcom.comfy_ui.file_management import hash_cache

class LocalFile(BaseModel):
    path: Path
    requires_editing: Optional[bool] = False

    @field_validator('path', mode='before')
    def _convert_path_str_to_path(cls, path_obj_or_str: Path | str) -> Path:
        if isinstance(path_obj_or_str, Path):
            return Path
        return Path(path_obj_or_str)
    
    @field_serializer('path')
    def _serialize_path(self, p: Path, info: SerializationInfo) -> str:
        return str(p)

    def __str__(self):
        return str("LocalFile(path={})".format(str(self.path_str)))
    
    @property
    def name(self) -> str:
        return self.path.name

    @property
    def path_str(self) -> str:
        return self.path.as_posix()

    @property
    def data(self):
        return open(self.path_str, 'rb').read()
    
    @property
    def exists(self) -> bool:
        return os.path.exists(self.path_str)

    @property
    def sha1(self):
        if self.exists:
            return hash_cache.sha1_hex_digest(self.data)
        return None
    
    @property
    def metadata_path(self):
        return self.path.with_suffix('.ccmeta').as_posix()

    @property
    def metadata_file_exists(self):
        return os.path.exists(self.metadata_path)