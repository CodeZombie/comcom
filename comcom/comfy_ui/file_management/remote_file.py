from dataclasses import dataclass

@dataclass
class RemoteFile:
    filename: str
    full_filepath: str
    subfolder: str = None