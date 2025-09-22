from typing import List
from dataclasses import dataclass

import json

from .node import Node

@dataclass
class Workflow:
    id: str
    version: int
    revision: int
    nodes: List[Node]

    def get_node_by_id(self, id: str) -> Node:
        print("get_node_by_id({})".format(id))
        return next((node for node in self.nodes if node.id == id), None)
    
    def get_nodes_by_title(self, title: str) -> List[Node]:
        results: List[Node] = []
        for node in self.nodes:
            if node.title == title:
                results.append(node)
        return results
    
    def as_api_dict(self):
        api_dict = dict()
        for node in self.nodes:
            api_dict[node.id] = node.as_api_dict(self.nodes)
        return api_dict

    def as_json(self):
        return json.dumps(self.as_api_dict())