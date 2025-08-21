from typing import List

from dataclasses import dataclass

from .input import Input

@dataclass
class Node:
    id: str
    type: str
    inputs: List[Input]