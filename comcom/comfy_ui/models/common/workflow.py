from typing import List
from dataclasses import dataclass

from .node import Node

@dataclass
class Workflow:
    name: str
    nodes: List[Node]