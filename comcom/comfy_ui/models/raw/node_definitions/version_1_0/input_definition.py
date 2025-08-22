from typing import Dict, List, Any
from pydantic import RootModel



class Comfy_v1_0_InputDefinition(RootModel[List[str | List | Dict[str, Any] | None]]):
    def __iter__(self):
        return iter(self.root)
    
    def __getitem__(self, name: str | int):
        return self.root[name]
    
    def __len__(self):
        return len(self.root)
    
    @property
    def type(self) -> str | None:
        
        if len(self) > 0:
            if isinstance(self[0], List):
                return "ENUM"
            else:
                return self[0]
        return None
            
    @property
    def metadata(self) -> Dict:
        if len(self) > 1:
            return self[1]
        return {}
