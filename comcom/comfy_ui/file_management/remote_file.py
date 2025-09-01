from pydantic import BaseModel
import urllib

class RemoteFile(BaseModel):
    filename: str
    type: str
    subfolder: str = None

    def get_full_uri(self, domain: str) -> str:
        return domain.rstrip('/') + "/view?" + urllib.parse.urlencode({"filename": self.filename, "subfolder": self.subfolder, "type": self.type})

    @property
    def api_name(self):
        if self.type:
            return "{} [{}]".format(self.filename, self.type.lower())
        return self.filename