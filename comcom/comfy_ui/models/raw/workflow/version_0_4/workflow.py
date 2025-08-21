from typing import Optional
from pydantic import BaseModel, Field, AliasPath

from .node import Comfy_V0_4_Node
from .subgraph_definition import Comfy_V0_4_SubgraphDefinition
from comcom.comfy_ui.models.normalized.workflow.workflow import NormalizedWorkflow

class Comfy_V0_4_Workflow(BaseModel):
    id: str
    revision: int
    nodes: list[Comfy_V0_4_Node]
    version: float
    subgraph_definitions: Optional[list[Comfy_V0_4_SubgraphDefinition]] = Field(validation_alias=AliasPath('definitions', 'subgraphs'), default=[])

    def to_normalized(self) -> NormalizedWorkflow:
        return NormalizedWorkflow(
            id=self.id,
            revision=self.revision,
            nodes=[node.to_normalized() for node in self.nodes],
            version=self.version,
            subgraph_definitions=[subgraph_definition.to_normalized() for subgraph_definition in self.subgraph_definitions]
        )
    
    def get_node(self, id: str):
        for node in self.nodes:
            if node.id == id:
                return node
        return None