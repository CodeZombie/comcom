from typing import Any
from functools import lru_cache
import hashlib

@lru_cache()
def sha1_hex_digest(data: Any):
    return hashlib.sha1(data).hexdigest()