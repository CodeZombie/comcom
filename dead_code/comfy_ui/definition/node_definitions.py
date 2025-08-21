from typing import Dict
from typing_extensions import Union
from pydantic import RootModel

from .node_definition import NodeDefinition

class NodeDefinitions(RootModel[Dict[str, NodeDefinition]]):
    def __getitem__(self, name: Union[str, int]):
        return self.root[name]
    
    def get_node_definition(self, type_name: str) -> NodeDefinition | None:
        for node_definition in self.root.values():
            if node_definition.name == type_name:
                return node_definition
        return None
