from typing import Optional
from pydantic import Field, AliasPath

from .subgraph_definition import SubgraphDefinition
from .abstract_graph import AbstractGraph

class ComfyWorkflow(AbstractGraph):
    subgraphs: Optional[list[SubgraphDefinition]] = Field(validation_alias=AliasPath('definitions', 'subgraphs'), default=[])
    
    def get_subgraph(self, subgraph_id: str) -> SubgraphDefinition:
        for subgraph in self.subgraphs:
            if subgraph.id == subgraph_id:
                return subgraph
    