from typing import Any, Dict

class AbstractSlot:
    @property
    def id() -> str:
        raise Exception("Not implemented")
    
    @property
    def type() -> str:
        raise Exception("Not implemented")
    
    @property
    def value() -> Any:
        raise Exception("Not implemented")

    @property
    def is_link() -> bool:
        raise Exception("Not implemented")
        
    @property
    def metadata() -> Dict:
        raise Exception("Not implemented")