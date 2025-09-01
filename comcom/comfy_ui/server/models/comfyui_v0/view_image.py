from dataclasses import dataclass
import urllib

class ComfyUI_v0_ViewImageResponse:
    filename: str
    subfolder: str
    type: str

    @property
    def endpoint(self):
        return f"view?{urllib.parse.urlencode({"filename": self.filename, "subfolder": self.subfolder, "type": self.type})}"