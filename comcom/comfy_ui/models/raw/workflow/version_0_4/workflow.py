from typing import Optional, List
from pydantic import BaseModel, Field, AliasPath

from .node import Comfy_V0_4_Node
from .subgraph_definition import Comfy_V0_4_SubgraphDefinition
from comcom.comfy_ui.models.normalized.workflow.workflow import NormalizedWorkflow
from comcom.comfy_ui.models.normalized.node_definition.node_definition import NormalizedNodeDefinition
from comcom.comfy_ui.models.normalized.workflow.subgraph_definition import NormalizedSubgraphDefinition

class Comfy_V0_4_Workflow(BaseModel):
    id: str
    revision: int
    nodes: list[Comfy_V0_4_Node]
    version: float
    subgraph_definitions: Optional[list[Comfy_V0_4_SubgraphDefinition]] = Field(validation_alias=AliasPath('definitions', 'subgraphs'), default=[])

    def to_normalized(self, node_definitions: List[NormalizedNodeDefinition]) -> NormalizedWorkflow:
        # Inject Subgraphs as NormalizedNodeDefinitions into the node_definitions list.
        subgraph_definitions_as_node_definitions: List[NormalizedNodeDefinition] = [subgraph_definition.to_node_definition() for subgraph_definition in self.subgraph_definitions]
        normalized_subgraph_definitions: List[NormalizedSubgraphDefinition] = [subgraph_definition.to_normalized(node_definitions + subgraph_definitions_as_node_definitions) for subgraph_definition in self.subgraph_definitions]
        node_definitions = node_definitions + [normalized_subgraph_definition.to_node_definition() for normalized_subgraph_definition in normalized_subgraph_definitions]
        
        return NormalizedWorkflow(
            id=self.id,
            revision=self.revision,
            nodes=[node.to_normalized(node_definitions) for node in self.nodes],
            version=self.version,
            subgraph_definitions=normalized_subgraph_definitions,
        )
    
    def get_node(self, id: str):
        for node in self.nodes:
            if node.id == id:
                return node
        return None